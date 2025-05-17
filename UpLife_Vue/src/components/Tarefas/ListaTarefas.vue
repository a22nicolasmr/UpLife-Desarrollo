<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  props: {
    dataSeleccionada: {
      type: Date,
      required: true,
    },
  },
  data() {
    return {
      tarefasPorData: {},
      tarefasConHora: {},
    };
  },
  computed: {
    //obter id de usuario do store
    usuarioStore() {
      return useUsuarioStore();
    },

    //filtrar tarefas por data
    tarefasFiltradasPorData() {
      const result = {};
      for (const [data, tarefas] of Object.entries(this.tarefasPorData)) {
        const nonCompletadas = tarefas.filter((t) => !t.completado);
        if (nonCompletadas.length > 0) {
          result[data] = nonCompletadas;
        }
      }
      return result;
    },
  },

  watch: {
    //cargar tareas cando cambia 'dataSeleccionada'
    dataSeleccionada: {
      immediate: true,
      handler(novaData) {
        this.cargarTarefas(novaData).then(() => {
          const dataISO = new Date(novaData).toLocaleDateString("en-CA");
          this.$nextTick(() => {
            const el = this.$refs["data-" + dataISO];
            const target = Array.isArray(el) ? el[0] : el;
          });
        });
      },
    },
    //tarefas cando cambia o usuario
    "usuarioStore.id": {
      immediate: true,
      handler() {
        // limpar estado das tarefas cando cambia o usuario
        this.tarefasPorData = {};
        this.tarefasConHora = {};
        if (this.dataSeleccionada) {
          this.cargarTarefas(this.dataSeleccionada);
        }
      },
    },
  },
  methods: {
    emitirDatasConTarefas(tarefasConHora) {
      this.$emit("datas-con-tarefas", tarefasConHora);
    },

    //cando se fai click nunha data con tarefas, facer scroll ata as tarefas
    scrollAtaData(data) {
      this.$nextTick(() => {
        const dataISO = new Date(data).toLocaleDateString("en-CA");
        const refs = this.$refs["data-" + dataISO];
        const scrollContainer = this.$refs.scrollArea;

        const bloque = Array.isArray(refs) ? refs[0] : refs;

        if (bloque && scrollContainer) {
          const bloqueRect = bloque.getBoundingClientRect();
          const containerRect = scrollContainer.getBoundingClientRect();

          const offset =
            bloqueRect.top - containerRect.top + scrollContainer.scrollTop;

          scrollContainer.scrollTo({
            top: offset,
            behavior: "smooth",
          });
        }
      });
    },

    //cargar as tarefas por data
    async cargarTarefas(data) {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      if (!data) return;
      const dataISO = new Date(data).toLocaleDateString("en-CA");

      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/tarefas/`
        );
        if (!response.ok) throw new Error("Erro ao cargar tarefas");
        const tarefas = await response.json();

        const hoyISO = new Date().toISOString().split("T")[0];
        this.tarefasConHora = tarefas.filter(
          (t) => t.usuario === idUsuario && t.hora != null && t.data === hoyISO
        );

        const agrupadas = {};
        const tarefasUsuario = tarefas.filter((t) => t.usuario === idUsuario);
        for (const tarefa of tarefasUsuario) {
          if (!agrupadas[tarefa.data]) agrupadas[tarefa.data] = [];
          agrupadas[tarefa.data].push(tarefa);
        }

        this.tarefasPorData = agrupadas;
        this.emitirDatasConTarefas(this.tarefasConHora);
      } catch (error) {
        console.error("Erro cargando tarefas:", error);
      }
    },

    //borrrar tarefa por id
    async borrarTarefa(id) {
      try {
        await fetch(`https://uplife-final.onrender.com/api/tarefas/${id}/`, {
          method: "DELETE",
        });

        for (const data in this.tarefasPorData) {
          this.tarefasPorData[data] = this.tarefasPorData[data].filter(
            (t) => t.id_tarefa !== id
          );

          // se o array esta vacío, eliminar o obxecto
          if (this.tarefasPorData[data].length === 0) {
            delete this.tarefasPorData[data];
            this.emitirDatasConTarefas();
          }
          this.$emit("cargarDatasConTarefas");
          // this.$emit("comprobarRachas");
        }
      } catch (error) {
        console.error("Erro ao borrar tarefa:", error);
      }
    },

    //marcar tarefa como completada
    async marcarCompletado(tarefa) {
      try {
        const updated = { completado: !tarefa.completado };
        const response = await fetch(
          `https://uplife-final.onrender.com/api/tarefas/${tarefa.id_tarefa}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updated),
          }
        );
        if (!response.ok) throw new Error("Erro ao actualizar tarefa");
        tarefa.completado = !tarefa.completado;
        this.$emit("comprobarRachas");
      } catch (error) {
        console.error("Erro ao marcar como completada:", error);
      }
    },

    //formatear a data
    formatoData(dataISO) {
      const [ano, mes, dia] = dataISO.split("-");
      return `${dia}/${mes}/${ano}`;
    },
  },
};
</script>

<template>
  <div class="lista-container">
    <h2 class="data-header">Tarefas pendentes</h2>

    <div class="scroll-area" ref="scrollArea">
      <div v-if="Object.keys(tarefasFiltradasPorData).length > 0">
        <div
          v-for="(tarefas, data) in tarefasFiltradasPorData"
          :key="data"
          :ref="'data-' + data"
        >
          <h3 class="data-header">{{ formatoData(data) }}</h3>
          <ul>
            <li
              v-for="tarefa in tarefas.filter((t) => !t.completado)"
              :key="tarefa.id_tarefa"
              class="tarefa-item"
            >
              <input
                type="checkbox"
                :checked="tarefa.completado"
                @change="marcarCompletado(tarefa)"
              />
              <span :class="{ feito: tarefa.completado }">
                {{ tarefa.hora?.slice(0, 5) || "--:--" }} - {{ tarefa.titulo }}
              </span>
              <button @click="borrarTarefa(tarefa.id_tarefa)">
                <img src="/imaxes/trash.png" alt="borrar" />
              </button>
            </li>
          </ul>
        </div>
      </div>
      <p v-else>Non hai tarefas pendentes.</p>
    </div>
  </div>
</template>

<style scoped>
.lista-container {
  color: white;
  background-color: black;
  padding: 8%;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 90%;
}

.scroll-area {
  max-height: 50vh;
  overflow-y: auto;
  padding-right: 2%;
}

.data-header {
  color: #7f5af0;
  margin-top: 4%;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tarefa-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #222;
  padding: 3%;
  border-radius: 8px;
  margin-bottom: 3%;
}

.tarefa-item span {
  flex: 1;
  margin-left: 4%;
}

.tarefa-item button {
  background: none;
  border: none;
  font-size: 1.5em;
  color: red;
  cursor: pointer;
}

.feito {
  text-decoration: line-through;
  color: #aaa;
}
</style>
