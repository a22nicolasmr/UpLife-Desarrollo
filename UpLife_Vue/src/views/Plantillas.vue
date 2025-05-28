<script>
import EngadirDoHistorial from "@/components/Plantillas/EngadirDoHistorial.vue";
import EngadirExercicioPlantilla from "@/components/Plantillas/EngadirExercicioPlantilla.vue";
import NovaPlantilla from "@/components/Plantillas/NovaPlantilla.vue";
import { useUsuarioStore } from "@/stores/useUsuario";
import draggable from "vuedraggable";

export default {
  components: {
    NovaPlantilla,
    EngadirExercicioPlantilla,
    draggable,
    EngadirDoHistorial,
  },
  data() {
    return {
      componenteActivo: "nova",
      plantillas: [],
      expandedPlantillas: [],
      plantillaSeleccionada: null,
      plantillaSeleccionadaMandar: null,
      editando: { id: null, campo: null, valor: "" },
      categoriasMap: {
        1: "Perna",
        2: "Brazo",
        3: "Core",
        4: "Espalda",
        5: "Peito",
        6: "Todo corpo",
      },
    };
  },
  computed: {
    // obter o id do usuario actual desde o store
    idUsuario() {
      return useUsuarioStore().id;
    },
    // obter o token actual desde o store
    token() {
      return useUsuarioStore().token;
    },
    // obter a data actual en formato ISO
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
  },
  mounted() {
    // cargar as plantillas ao montar o compoñente
    this.cargarDatos();
  },
  methods: {
    // obter o nome da categoría a partir do seu id
    nomeCategoriaPorId(id) {
      return this.categoriasMap[id] || "Descoñecida";
    },

    // cargar as plantillas do usuario
    async cargarDatos() {
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas/",
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );
        if (!response.ok) throw new Error("Erro ao cargar plantillas");
        const plantillas = await response.json();
        this.plantillas = plantillas
          .filter((p) => p.usuario === this.idUsuario)
          .map((p) => ({
            ...p,
            exercicios: (p.exercicios || []).sort(
              (a, b) => a.id_exercicio - b.id_exercicio
            ),
          }));
      } catch (error) {
        console.error("Erro cargando datos:", error);
      }
    },

    // eliminar unha plantilla e os seus exercicios
    async borrarPlantilla(id) {
      try {
        const plantilla = this.plantillas.find((p) => p.id_plantilla === id);
        if (!plantilla) throw new Error("Plantilla non atopada");

        const exercicios = plantilla.exercicios || [];
        for (const ex of exercicios) {
          const res = await fetch(
            `https://uplife-final.onrender.com/api/exercicios/${ex.id_exercicio}/`,
            {
              method: "DELETE",
              headers: { Authorization: `Bearer ${this.token}` },
            }
          );
          if (!res.ok)
            throw new Error(`Erro ao eliminar exercicio ${ex.id_exercicio}`);
        }

        const response = await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${id}/`,
          {
            method: "DELETE",
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );
        if (!response.ok) throw new Error("Erro ao eliminar plantilla");

        this.plantillas = this.plantillas.filter((p) => p.id_plantilla !== id);
        this.componenteActivo = "nova";
      } catch (error) {
        console.error("Erro eliminando plantilla e exercicios:", error);
      }
    },

    // expandir ou contraer unha plantilla
    toggleExpand(id) {
      this.expandedPlantillas = this.expandedPlantillas.includes(id)
        ? this.expandedPlantillas.filter((pid) => pid !== id)
        : [...this.expandedPlantillas, id];
    },

    // eliminar un exercicio polo seu id
    async borrarExercicio(idExercicio, idPlantilla) {
      try {
        // Obtener la plantilla
        const res = await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${idPlantilla}/`,
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );
        if (!res.ok) throw new Error("Non se puido obter a plantilla");

        const plantilla = await res.json();

        // Obtener solo os IDs dos exercicios, excluíndo o que se vai borrar
        const idsActualizados = (plantilla.exercicios || [])
          .map((e) => (typeof e === "object" ? e.id_exercicio : e))
          .filter((id) => id !== idExercicio);

        // Actualizar a plantilla sen ese exercicio
        const patchRes = await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${idPlantilla}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify({ exercicios: idsActualizados }),
          }
        );

        if (!patchRes.ok)
          throw new Error("Erro ao actualizar a plantilla sen o exercicio");

        // Actualizar datos localmente
        const plantillaLocal = this.plantillas.find(
          (p) => p.id_plantilla === idPlantilla
        );
        if (plantillaLocal) {
          plantillaLocal.exercicios = plantillaLocal.exercicios.filter(
            (e) => e.id_exercicio !== idExercicio
          );
        }
      } catch (error) {
        console.error("Erro eliminando exercicio da plantilla:", error);
      }
    },
    // activar o modo engadir exercicio e expandir a plantilla correspondente
    engadirExercicio(plantilla) {
      this.componenteActivo = "engadirE";
      this.plantillaSeleccionadaMandar = plantilla.id_plantilla;
      this.toggleExpand(plantilla.id_plantilla);
    },

    // activar edición dun campo dun exercicio
    activarEdicion(id, campo) {
      if (this.editando.id === id && this.editando.campo === campo) return;
      this.editando = { id, campo, valor: this.getExercicioValue(id, campo) };
    },

    // obter valor actual dun campo para edición
    getExercicioValue(id, campo) {
      for (const plantilla of this.plantillas) {
        const exerciciosOrdenados = [...plantilla.exercicios].sort(
          (a, b) => a.id_exercicio - b.id_exercicio
        );
        const ex = exerciciosOrdenados.find((e) => e.id_exercicio === id);
        if (ex) return ex[campo];
      }
      return "";
    },

    // gardar os cambios dun campo editado
    async guardarCampoEditado(id, campo) {
      const novoValor = this.editando.valor;
      this.editando = { id: null, campo: null, valor: "" };
      try {
        await fetch(`https://uplife-final.onrender.com/api/exercicios/${id}/`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`,
          },
          body: JSON.stringify({ [campo]: novoValor }),
        });
        this.cargarDatos();
      } catch (error) {
        console.error("Erro ao actualizar exercicio:", error);
      }
    },

    // gardar a nova orde dos exercicios nunha plantilla
    async guardarNovaOrden(plantilla) {
      const novaLista = plantilla.exercicios.map((e) => e.id_exercicio);
      try {
        await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${plantilla.id_plantilla}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify({ exercicios: novaLista }),
          }
        );
      } catch (error) {
        console.error("Erro ao gardar nova orde:", error);
      }
    },
  },
};
</script>

<template>
  <div id="divXeral2">
    <h1 class="titulo">Plantillas</h1>

    <div class="tarxetas">
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'nova' }"
        @click="componenteActivo = 'nova'"
      >
        Nova
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadirE' }"
        @click="componenteActivo = 'engadirE'"
      >
        Engadir
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadirD' }"
        @click="componenteActivo = 'engadirD'"
      >
        Engadir exercicio do historial
      </div>
    </div>

    <div class="plantilla-layout">
      <div class="esquerda">
        <h2>Lista de plantillas</h2>
        <div
          v-for="plantilla in plantillas"
          :key="plantilla.id_plantilla"
          class="divPlantilla"
        >
          <div class="plantilla-header">
            <img :src="plantilla.icona" alt="icona plantilla" />
            <h3>{{ plantilla.nome }}</h3>
            <div class="botons-container">
              <button
                class="expand-button"
                @click.stop="toggleExpand(plantilla.id_plantilla)"
                :class="{
                  rotated: expandedPlantillas.includes(plantilla.id_plantilla),
                }"
              >
                ▼
              </button>
              <button class="button-add" @click="engadirExercicio(plantilla)">
                +
              </button>
              <img
                src="/imaxes/trash.png"
                alt="icona borrar"
                class="icono-trash"
                @click="borrarPlantilla(plantilla.id_plantilla)"
              />
            </div>
          </div>

          <transition name="fade-slide">
            <div
              v-if="expandedPlantillas.includes(plantilla.id_plantilla)"
              class="exercicios-plantilla"
            >
              <template
                v-if="plantilla.exercicios && plantilla.exercicios.length"
              >
                <table class="tabela-exercicios">
                  <thead>
                    <tr>
                      <th>Nome</th>
                      <th>Repeticións</th>
                      <th>Peso (kg)</th>
                      <th>Categoria</th>
                      <th>Eliminar</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="ex in plantilla.exercicios"
                      :key="ex.id_exercicio"
                    >
                      <td @click="activarEdicion(ex.id_exercicio, 'nome')">
                        <input
                          v-if="
                            editando.id === ex.id_exercicio &&
                            editando.campo === 'nome'
                          "
                          v-model="editando.valor"
                          @blur="guardarCampoEditado(ex.id_exercicio, 'nome')"
                          @keyup.enter="
                            guardarCampoEditado(ex.id_exercicio, 'nome')
                          "
                          @click.stop
                        />
                        <span v-else>{{ ex.nome }}</span>
                      </td>

                      <td
                        @click="activarEdicion(ex.id_exercicio, 'repeticions')"
                      >
                        <input
                          v-if="
                            editando.id === ex.id_exercicio &&
                            editando.campo === 'repeticions'
                          "
                          v-model="editando.valor"
                          @blur="
                            guardarCampoEditado(ex.id_exercicio, 'repeticions')
                          "
                          @keyup.enter="
                            guardarCampoEditado(ex.id_exercicio, 'repeticions')
                          "
                          @click.stop
                        />
                        <span v-else>{{ ex.repeticions }}</span>
                      </td>

                      <td @click="activarEdicion(ex.id_exercicio, 'peso')">
                        <input
                          v-if="
                            editando.id === ex.id_exercicio &&
                            editando.campo === 'peso'
                          "
                          type="number"
                          v-model.number="editando.valor"
                          @blur="guardarCampoEditado(ex.id_exercicio, 'peso')"
                          @keyup.enter="
                            guardarCampoEditado(ex.id_exercicio, 'peso')
                          "
                          @click.stop
                        />
                        <span v-else>{{ ex.peso }}</span>
                      </td>

                      <td @click="activarEdicion(ex.id_exercicio, 'categoria')">
                        <select
                          v-if="
                            editando.id === ex.id_exercicio &&
                            editando.campo === 'categoria'
                          "
                          v-model.number="editando.valor"
                          @blur="
                            guardarCampoEditado(ex.id_exercicio, 'categoria')
                          "
                          @keyup.enter="
                            guardarCampoEditado(ex.id_exercicio, 'categoria')
                          "
                          @click.stop
                        >
                          <option
                            v-for="(label, key) in categoriasMap"
                            :value="parseInt(key)"
                            :key="key"
                          >
                            {{ label }}
                          </option>
                        </select>
                        <span v-else>{{
                          nomeCategoriaPorId(ex.categoria)
                        }}</span>
                      </td>

                      <td>
                        <img
                          src="/imaxes/trash.png"
                          alt="borrar exercicio"
                          class="icono-trash"
                          @click="
                            borrarExercicio(
                              ex.id_exercicio,
                              plantilla.id_plantilla
                            )
                          "
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
              </template>

              <p v-else class="sen-exercicios">
                Esta plantilla non ten exercicios.
              </p>
            </div>
          </transition>
        </div>
        <button @click="componenteActivo = 'nova'" id="engadirE">+</button>
      </div>

      <div class="dereita">
        <NovaPlantilla
          v-if="componenteActivo === 'nova'"
          @cargarDatos="cargarDatos"
        />
        <EngadirExercicioPlantilla
          v-if="componenteActivo === 'engadirE'"
          :plantillaSeleccionadaMandar="plantillaSeleccionadaMandar"
          @cargarDatos="cargarDatos"
          ref="engadirRef"
        />
        <EngadirDoHistorial
          v-if="componenteActivo === 'engadirD'"
          @cargarDatos="cargarDatos"
        >
        </EngadirDoHistorial>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tabela-exercicios {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.tabela-exercicios th,
.tabela-exercicios td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: center;
  font-size: medium;
}

.tabela-exercicios th {
  background-color: #7f5af0;
  font-weight: bold;
  color: white;
}

.exercicio-datos {
  display: flex;
  flex-direction: row;
  color: black;
  gap: 4px;
}

.plantilla-header img:first-child {
  background-color: white;
  border-radius: 8px;
}

.button {
  background-color: #d8d8d8;
  color: #7f5af0;
  font-size: xx-large;
  display: flex;
  justify-self: center;
}

.expand-button {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.expand-button.rotated {
  transform: rotate(180deg);
}

.divPlantilla {
  background-color: #d8d8d8;
  border-radius: 8px;
  margin-bottom: 2%;
  padding: 1%;
  display: flex;
  flex-direction: column;
  position: relative;
  box-sizing: border-box;
}

.plantilla-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  box-sizing: border-box;
  width: 100%;
}

.plantilla-header img:first-child {
  height: 8%;
  width: 8%;
}

#divXeral2 {
  display: flex;
  flex-direction: column;
  height: auto;
  overflow-x: hidden;
}

.titulo {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
  color: #7f5af0;
  margin-bottom: 0;
}
h2 {
  color: #7f5af0;
}

.tarxetas {
  display: flex;
  justify-content: center;
}

.tarxeta {
  background-color: #4880ff;
  color: white;
  padding: 1% 2%;
  border-radius: 1vh 1vh 0 0;
  cursor: pointer;
  font-weight: bold;
  font-size: medium;
  transition: 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.inactiva {
  background-color: #d8d8d8;
  color: #fff;
}

.plantilla-layout {
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  margin-bottom: 2%;
  height: auto;
  overflow: visible;
}

.esquerda {
  width: 60%;
  padding: 2%;
  box-sizing: border-box;
  height: auto;
  overflow: visible;
}

.dereita {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
  height: auto;
  overflow: visible;
  border-radius: 0 0 8px 8px;
}

button {
  margin-top: 3%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 9%;
}

#engadirE {
  font-size: xx-large;
}

.exercicios-plantilla {
  width: 100%;
  margin-top: 1%;
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 8px;
  box-sizing: border-box;
  overflow: hidden;
}

.exercicio {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
  color: black;
  padding: 4px 0;
  box-sizing: border-box;
}

.sen-exercicios {
  font-style: italic;
  color: #777;
}

.icono-borrar-ex {
  width: 2%;
  height: 2%;
  cursor: pointer;
  margin-left: 8px;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  max-height: 500px;
  opacity: 1;
  transform: translateY(0);
}

.botons-container {
  display: flex;
  justify-content: space-between;
}

.button-add {
  background-color: #d8d8d8;
  color: #7f5af0;
  font-size: xx-large;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.icono-trash {
  width: 18%;
  height: 18%;
  cursor: pointer;
  margin-top: 22%;
}

@media (max-width: 768px) {
  img {
    margin-right: 5%;
  }
  .plantilla-layout {
    flex-direction: column;
    width: 100%;
    height: auto !important;
    overflow: visible !important;
    margin: 0;
    padding: 0;
  }

  .esquerda,
  .dereita {
    width: 100%;
    height: auto !important;
    overflow: visible !important;
    padding: 1rem;
    box-sizing: border-box;
  }

  #divXeral2 {
    height: auto;
    overflow-y: visible;
    padding-bottom: 2rem;
  }

  .tarxetas {
    display: flex;
    width: 100%;
    justify-content: center;
    flex-direction: row;
    gap: 1%;
    margin-top: 1rem;
  }

  .tarxeta {
    font-size: 0.9rem;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem 0.5rem 0 0;
    box-shadow: none;
    margin: 0;
  }

  .tarxeta.inactiva {
    background-color: #ccc;
    color: #fff;
  }

  .tabela-exercicios {
    min-width: 600px;
    font-size: 0.85rem;
  }

  .exercicios-plantilla {
    overflow-x: auto;
  }

  .expand-button {
    font-size: 1.2rem;
    width: 1.8rem;
    height: 1.8rem;
    margin: 0;
  }

  .button-add {
    font-size: 1.5rem;
    height: 2rem;
    margin: 0;
    padding-left: 0;
    margin-top: -5%;
    margin-right: -5%;
    margin-left: -10%;
  }

  .icono-trash {
    width: 1rem;
    height: 1rem;
    margin-top: 15%;
  }

  .plantilla-header img:first-child {
    width: 2.5rem;
    height: 2.5rem;
  }

  button#engadirE {
    width: 100%;
    font-size: 1.5rem;
    padding: 1rem;
    margin-top: 1.5rem;
  }

  body {
    overflow-x: hidden;
  }

  .expand-button {
    margin-left: 20%;
    margin-top: 10%;
  }
}

@media (min-width: 769px) and (max-width: 1370px) {
  img {
    margin-right: 5%;
  }
  .plantilla-layout {
    flex-direction: column;
    width: 100%;
    height: auto !important;
    overflow: visible !important;
    margin: 0;
    padding: 0;
  }

  .esquerda,
  .dereita {
    width: 100%;
    height: auto !important;
    overflow: visible !important;
    padding: 1rem;
    box-sizing: border-box;
  }

  #divXeral2 {
    height: auto;
    overflow-y: visible;
    padding-bottom: 2rem;
  }

  .tarxetas {
    display: flex;
    width: 100%;
    justify-content: center;
    flex-direction: row;
    gap: 1%;
    margin-top: 1rem;
  }

  .tarxeta {
    font-size: 0.9rem;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem 0.5rem 0 0;
    box-shadow: none;
    margin: 0;
  }

  .tarxeta.inactiva {
    background-color: #ccc;
    color: #fff;
  }

  .tabela-exercicios {
    min-width: 600px;
    font-size: 0.85rem;
  }

  .exercicios-plantilla {
    overflow-x: auto;
  }

  .expand-button {
    font-size: 1.2rem;
    width: 1.8rem;
    height: 1.8rem;
    margin: 0;
  }

  .button-add {
    font-size: 1.5rem;
    height: 2rem;
    margin: 0;
    padding-left: 0;
    margin-top: -5%;
    margin-right: -5%;
    margin-left: -10%;
  }

  .icono-trash {
    width: 1rem;
    height: 1rem;
    margin-top: 15%;
  }

  .plantilla-header img:first-child {
    width: 2.5rem;
    height: 2.5rem;
  }

  button#engadirE {
    width: 100%;
    font-size: 1.5rem;
    padding: 1rem;
    margin-top: 1.5rem;
  }

  body {
    overflow-x: hidden;
  }

  .expand-button {
    margin-left: 20%;
    margin-top: 10%;
  }
}
</style>
