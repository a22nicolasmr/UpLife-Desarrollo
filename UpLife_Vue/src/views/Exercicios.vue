<script>
import EngadirExercicios from "@/components/Exercicios/EngadirExercicios.vue";
import EngadirPlantillasExercicios from "@/components/Exercicios/EngadirPlantillasExercicios.vue";
import HistorialExercicios from "@/components/Exercicios/HistorialExercicios.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    HistorialExercicios,
    EngadirExercicios,
    EngadirPlantillasExercicios,
  },
  data() {
    return {
      componenteActivo: "historial",
      exerciciosHoxe: [],
      plantillasHoxe: [],
      expandedPlantillas: [],
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
  mounted() {
    this.cargarExerciciosHoxe();
    this.cargarPlantillasHoxe();
    document.addEventListener("click", this.cancelarEdicionAoFora);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.cancelarEdicionAoFora);
  },
  methods: {
    nomeCategoriaPorId(id) {
      return this.categoriasMap[id] || "Descoñecida";
    },
    async cargarExerciciosHoxe() {
      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch("http://localhost:8001/api/exercicios/");
        const exercicios = await response.json();
        this.exerciciosHoxe = exercicios.filter(
          (ex) => ex.usuario === idUsuario && ex.data === hoxe
        );
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro cargando exercicios:", error);
      }
    },
    async eliminarExercicio(id) {
      try {
        await fetch(`http://localhost:8001/api/exercicios/${id}/`, {
          method: "DELETE",
        });
        this.cargarExerciciosHoxe();
        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro eliminando exercicio:", error);
      }
    },
    // Métodos para edición
    activarEdicion(id, campo, valor) {
      this.editando = { id, campo, valor };
    },
    cancelarEdicionAoFora(e) {
      if (!e.target.closest(".editable")) {
        this.editando = { id: null, campo: null, valor: "" };
      }
    },
    async guardarCampoEditado(id, campo) {
      const rawValor = this.editando.valor;
      let valorConvertido;

      // ✅ Convertir solo si el campo necesita tipo numérico
      if (campo === "peso") {
        valorConvertido = parseFloat(rawValor);
        if (isNaN(valorConvertido)) {
          console.warn(`Valor non válido para ${campo}:`, rawValor);
          return;
        }
      } else if (campo === "categoria") {
        valorConvertido = parseInt(rawValor, 10);
        if (isNaN(valorConvertido)) {
          console.warn(`Valor non válido para categoría:`, rawValor);
          return;
        }
      } else {
        // ✅ Mantén strings como están (ej: repeticions = "5x10")
        valorConvertido = String(rawValor);
      }

      try {
        const response = await fetch(
          `http://localhost:8001/api/exercicios/${id}/`,
          {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ [campo]: valorConvertido }),
          }
        );

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.warn("Resposta con erro (pero quizais aplicada):", errorData);
        }

        // Limpar estado de edición
        this.editando = { id: null, campo: null, valor: "" };

        // Volver cargar datos actualizados
        this.cargarExerciciosHoxe();
        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro ao actualizar exercicio:", error);
      }
    },
    async cargarPlantillasHoxe() {
      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch("http://localhost:8001/api/plantillas/");
        const plantillas = await response.json();
        this.plantillasHoxe = plantillas
          .filter((p) => p.usuario === idUsuario && p.data === hoxe)
          .map((p) => ({ ...p, exercicios: p.exercicios || [] }));
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro cargando plantillas hoxe:", error);
      }
    },
    toggleExpandPlantilla(id) {
      if (this.expandedPlantillas.includes(id)) {
        this.expandedPlantillas = this.expandedPlantillas.filter(
          (pid) => pid !== id
        );
      } else {
        this.expandedPlantillas.push(id);
      }
    },
    async engadirPlantilla(nomePlantilla) {
      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch("http://localhost:8001/api/plantillas/");
        const plantillas = await response.json();
        const plantilla = plantillas.find(
          (p) => p.usuario === idUsuario && p.nome === nomePlantilla
        );
        await fetch(
          `http://localhost:8001/api/plantillas/${plantilla.id_plantilla}/`,
          {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ data: hoxe }),
          }
        );
        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro engadindo plantilla:", error);
      }
    },
    async eliminarPlantilla(id_plantilla) {
      try {
        await fetch(`http://localhost:8001/api/plantillas/${id_plantilla}/`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ data: null }),
        });
        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro eliminando plantilla:", error);
      }
    },
  },
};
</script>

<template>
  <div id="divXeral2">
    <h1 class="titulo">Exercicios</h1>
    <div class="tarxetas">
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'historial' }"
        @click="componenteActivo = 'historial'"
      >
        Historial
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadirE' }"
        @click="componenteActivo = 'engadirE'"
      >
        Engadir exercicios
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadirP' }"
        @click="componenteActivo = 'engadirP'"
      >
        Engadir plantillas
      </div>
    </div>

    <div class="exercicios-layout">
      <div class="esquerda">
        <div class="esquerdaArriba">
          <h2>Exercicios de hoxe</h2>
        </div>
        <div class="esquerdaAbaixo">
          <table>
            <thead>
              <tr>
                <th>Título</th>
                <th>Categoría</th>
                <th>Repeticións</th>
                <th>Peso</th>
                <th>Eliminar</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="exercicio in exerciciosHoxe"
                :key="exercicio.id_exercicio"
              >
                <!-- Nome -->
                <td
                  @click="
                    activarEdicion(
                      exercicio.id_exercicio,
                      'nome',
                      exercicio.nome
                    )
                  "
                  class="editable"
                >
                  <input
                    v-if="
                      editando.id === exercicio.id_exercicio &&
                      editando.campo === 'nome'
                    "
                    v-model="editando.valor"
                    @blur="guardarCampoEditado(exercicio.id_exercicio, 'nome')"
                    @keyup.enter="
                      guardarCampoEditado(exercicio.id_exercicio, 'nome')
                    "
                    @click.stop
                  />
                  <span v-else>{{ exercicio.nome }}</span>
                </td>

                <!-- Categoría -->
                <td
                  @click="
                    activarEdicion(
                      exercicio.id_exercicio,
                      'categoria',
                      exercicio.categoria
                    )
                  "
                  class="editable"
                >
                  <select
                    v-if="
                      editando.id === exercicio.id_exercicio &&
                      editando.campo === 'categoria'
                    "
                    v-model.number="editando.valor"
                    @blur="
                      guardarCampoEditado(exercicio.id_exercicio, 'categoria')
                    "
                    @keyup.enter="
                      guardarCampoEditado(exercicio.id_exercicio, 'categoria')
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
                    nomeCategoriaPorId(exercicio.categoria)
                  }}</span>
                </td>

                <!-- Repeticións -->
                <td
                  @click="
                    activarEdicion(
                      exercicio.id_exercicio,
                      'repeticions',
                      exercicio.repeticions
                    )
                  "
                  class="editable"
                >
                  <input
                    v-if="
                      editando.id === exercicio.id_exercicio &&
                      editando.campo === 'repeticions'
                    "
                    v-model="editando.valor"
                    @blur="
                      guardarCampoEditado(exercicio.id_exercicio, 'repeticions')
                    "
                    @keyup.enter="
                      guardarCampoEditado(exercicio.id_exercicio, 'repeticions')
                    "
                    @click.stop
                  />
                  <span v-else>{{ exercicio.repeticions }}</span>
                </td>

                <!-- Peso -->
                <td
                  @click="
                    activarEdicion(
                      exercicio.id_exercicio,
                      'peso',
                      exercicio.peso
                    )
                  "
                  class="editable"
                >
                  <input
                    v-if="
                      editando.id === exercicio.id_exercicio &&
                      editando.campo === 'peso'
                    "
                    v-model.number="editando.valor"
                    @blur="guardarCampoEditado(exercicio.id_exercicio, 'peso')"
                    @keyup.enter="
                      guardarCampoEditado(exercicio.id_exercicio, 'peso')
                    "
                    @click.stop
                  />
                  <span v-else>{{ exercicio.peso }} </span>
                </td>

                <!-- Eliminar -->
                <td>
                  <img
                    src="/imaxes/trash.png"
                    alt="icona borrar"
                    @click="eliminarExercicio(exercicio.id_exercicio)"
                    class="icon2"
                  />
                </td>
              </tr>
              <tr v-if="exerciciosHoxe.length === 0">
                <td colspan="4">Non hai exercicios rexistrados para hoxe.</td>
              </tr>
            </tbody>
          </table>
          <button @click="componenteActivo = 'engadirE'">+</button>
        </div>

        <!-- NOVA TÁBOA DE PLANTILLAS -->
        <div class="esquerdaAbaixo">
          <h2>Plantillas de hoxe</h2>
          <table>
            <thead>
              <tr>
                <th>Icona</th>
                <th>Nome</th>
                <th>Eliminar</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="plantilla in plantillasHoxe"
                :key="plantilla.id_plantilla"
              >
                <td>
                  <img
                    :src="plantilla.icona"
                    alt="icona plantilla"
                    class="icona"
                  />
                </td>
                <td>{{ plantilla.nome }}</td>
                <td>
                  <img
                    src="/imaxes/trash.png"
                    alt="icona borrar"
                    @click="eliminarPlantilla(plantilla.id_plantilla)"
                    class="icon"
                  />
                </td>
              </tr>
              <tr v-if="plantillasHoxe.length === 0">
                <td colspan="3">Non hai plantillas rexistradas para hoxe.</td>
              </tr>
            </tbody>
          </table>
          <button @click="componenteActivo = 'engadirP'">+</button>
        </div>
      </div>

      <div class="dereita">
        <HistorialExercicios
          v-if="componenteActivo === 'historial'"
          @cargarExerciciosHoxe="cargarExerciciosHoxe"
          @cargarPlantillasHoxe="cargarPlantillasHoxe"
          ref="historialRef"
        />
        <EngadirExercicios
          v-if="componenteActivo === 'engadirE'"
          @cargarExerciciosHoxe="cargarExerciciosHoxe"
        />
        <EngadirPlantillasExercicios
          v-if="componenteActivo === 'engadirP'"
          @engadirPlantilla="engadirPlantilla"
          @cargarPlantillasHoxe="cargarPlantillasHoxe"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.icon {
  height: 10%;
  width: 10%;
  cursor: pointer;
}
.icon2 {
  height: 15%;
  width: 15%;
  cursor: pointer;
}
.icona {
  height: 20%;
  width: 20%;
  background: white;
  border-radius: 4px;
}
#engadirE {
  font-size: xx-large;
}
#engadirPbutton {
  font-size: smaller;
  width: 25%;
}
.esquerdaAbaixo {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 100%;
}
table {
  width: 100%;
}
tr {
  display: flex;
  justify-content: space-around;
}
.esquerdaArriba {
  display: flex;
  justify-content: space-between;
  margin-left: 2%;
  margin-right: 2%;
}
button {
  margin-top: 3%;
  padding: 1%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 9%;
  height: 5%;
}
html,
body {
  height: 100%;
  width: 100%;
}

#divXeral2 {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
  margin: none;
}

.titulo {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
  margin-bottom: 0;
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

.exercicios-layout {
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  margin-bottom: 1%;
  height: 100%;
  overflow: hidden;
}

.esquerda {
  width: 60%;
  height: 100%;
  overflow-y: auto;
  padding: 1%;
  box-sizing: border-box;
  overflow-x: hidden;
}

.esquerdaAbaixo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  padding: 2%;
}

h2 {
  color: #7f5af0;
}
h1 {
  display: flex;
  align-self: flex-start;
  font-size: 2vw;
  margin-bottom: 3vh;
  color: #7f5af0;
}
/* Compoñente dereita */
.dereita {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
  overflow-y: auto;
}

table {
  width: 96%;
  border-collapse: collapse;
  background-color: #d8d8d8;
  color: black;
  border-radius: 8px;
  overflow: hidden;
  margin: 0;
}

th,
td {
  padding: 2%;
  text-align: center;
  flex: 1;
}

thead {
  background-color: #7f5af0;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}

tbody tr {
  border-bottom: 1% solid #acacac;
}

tr {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

td[colspan="4"],
td[colspan="3"] {
  text-align: center;
  color: #aaa;
  font-style: italic;
}

/* Estilos para edición */
.editable {
  cursor: pointer;
  position: relative;
}

.editable:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.editable input,
.editable select {
  width: 100%;
  padding: 4px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: inherit;
  text-align: center;
}

.editable select {
  padding: 3px;
}
</style>
