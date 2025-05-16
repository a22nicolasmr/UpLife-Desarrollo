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
    activarEdicion(id, campo, valor) {
      this.editando = { id, campo, valor };
      // Espera a que se renderice el input y luego lo enfoca
      this.$nextTick(() => {
        const input = this.$el.querySelector("input:focus, select:focus");
        if (input) input.focus();
      });
    },

    async guardarCampoEditado(id, campo) {
      const novoValor = this.editando.valor;
      this.editando = { id: null, campo: null, valor: "" };
      try {
        await fetch(`https://uplife-final.onrender.com/api/exercicios/${id}/`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ [campo]: novoValor }),
        });
        this.cargarExerciciosHoxe(); // recargar lista
      } catch (error) {
        console.error("Erro ao actualizar exercicio:", error);
      }
    },

    cancelarEdicionAoFora(e) {
      const path = e.composedPath?.() || e.path || [];
      const clickedInsideInput = path.some((el) =>
        el?.classList?.contains("editable")
      );
      if (!clickedInsideInput) {
        this.editando = { id: null, campo: null, valor: "" };
      }
    },
    nomeCategoriaPorId(id) {
      return this.categoriasMap[id] || "Descoñecida";
    },
    async cargarExerciciosHoxe() {
      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/exercicios/"
        );
        const exercicios = await response.json();
        this.exerciciosHoxe = exercicios.filter(
          (ex) => ex.usuario === idUsuario && ex.data === hoxe
        );
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro cargando exercicios:", error);
      }
    },
    async cargarPlantillasHoxe() {
      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas-uso/"
        );
        const usos = await response.json();

        const usosFiltrados = usos.filter(
          (uso) => uso.usuario === idUsuario && uso.data === hoxe
        );

        // Cargar los detalles de cada plantilla por su ID
        const plantillasCompletas = await Promise.all(
          usosFiltrados.map(async (uso) => {
            const plantillaResponse = await fetch(
              `https://uplife-final.onrender.com/api/plantillas/${uso.plantilla}/`
            );
            const plantillaData = await plantillaResponse.json();
            return {
              id_plantilla: plantillaData.id_plantilla,
              nome: plantillaData.nome,
              icona: plantillaData.icona,
            };
          })
        );
        this.plantillasHoxe = plantillasCompletas;

        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro cargando plantillas hoxe:", error);
      }
    },
    async eliminarPlantilla(id_plantilla) {
      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas-uso/"
        );
        const usos = await response.json();

        const uso = usos.find(
          (u) =>
            u.plantilla === id_plantilla &&
            u.usuario === idUsuario &&
            u.data === hoxe
        );

        if (!uso) return;

        await fetch(
          `https://uplife-final.onrender.com/api/plantillas-uso/${uso.id}/`,
          {
            method: "DELETE",
          }
        );

        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro eliminando plantilla:", error);
      }
    },
    async engadirPlantilla(nomePlantilla) {
      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas/"
        );
        const plantillas = await response.json();
        const plantilla = plantillas.find(
          (p) => p.usuario === idUsuario && p.nome === nomePlantilla
        );
        console.log("id plantilla", plantilla.id_plantilla);

        await fetch("https://uplife-final.onrender.com/api/plantillas-uso/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            usuario: idUsuario,
            plantilla: plantilla.id_plantilla,
            data: hoxe,
          }),
        });

        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro engadindo plantilla:", error);
      }
    },
    async eliminarExercicio(id) {
      try {
        await fetch(`https://uplife-final.onrender.com/api/exercicios/${id}/`, {
          method: "DELETE",
        });
        this.cargarExerciciosHoxe();
        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro eliminando exercicio:", error);
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
  overflow: hidden; /* se actualiza en móvil */
}

.esquerda,
.dereita {
  height: 100%;
  overflow-y: auto;
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

@media (max-width: 768px) {
  /* CONTENEDORES */
  .exercicios-layout {
    flex-direction: column;
    height: auto !important;
    overflow: visible !important;
    width: 100%;
    margin-right: 0;
  }

  .esquerda,
  .dereita {
    width: 100%;
    height: auto !important;
    overflow: visible !important; /* ✅ Elimina scroll interno */
    padding: 1rem;
    box-sizing: border-box;
  }

  .esquerdaAbaixo {
    width: 100%;
    overflow-x: auto; /* ✅ Solo scroll horizontal si es necesario */
    padding: 0;
  }

  .esquerdaArriba {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  /* TABLAS MÁS COMPACTAS PERO LEGIBLES */
  table {
    width: 100%;
    min-width: 480px; /* ✅ Previene que el contenido colapse */
    border-collapse: collapse;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-bottom: 1rem;
    table-layout: auto;
  }

  thead {
    background-color: #7f5af0;
    color: white;
  }

  th,
  td {
    padding: 0.5rem;
    text-align: center;
    border-bottom: 1px solid #ddd;
    font-size: 0.7rem; /* ✅ Más legible */
    word-break: break-word;
  }

  td {
    background-color: #f9f9f9;
    width: 1.25rem;
    height: 1.25rem;
  }

  /* BOTÓN ESTILO COMPACTO */
  button {
    width: 100%;
    font-size: 1rem;
    padding: 0.75rem;
    margin-top: 0.75rem;
    background-color: #4880ff;
    color: white;
    border: none;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* ICONOS AJUSTADOS */
  .icon,
  .icon2 {
    width: 0.5rem;
    height: 0.5rem;
  }

  .icona,
  .icon,
  .icon2 {
    width: 1.25rem;
    height: 1.25rem;
    object-fit: contain;
  }

  /* TARXETAS NAVEGACIÓN */
  .tarxetas {
    display: flex;
    width: 100%;
    justify-content: center;
    flex-direction: row;
    gap: 1%;
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

  /* TÍTULOS */
  h1 {
    font-size: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
  }

  h2 {
    font-size: 1rem;
    margin: 0.75rem 0 0.5rem;
  }
}
</style>
