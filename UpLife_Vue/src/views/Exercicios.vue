<script>
import EngadirExercicios from "@/components/Exercicios/EngadirExercicios.vue";
import EngadirPlantillasExercicios from "@/components/Exercicios/EngadirPlantillasExercicios.vue";
import HistorialExercicios from "@/components/Exercicios/HistorialExercicios.vue";
import { useUsuarioStore } from "@/stores/useUsuario";
import Cargando from "@/components/BarrasNavegacion/Cargando.vue";

export default {
  components: {
    HistorialExercicios,
    EngadirExercicios,
    EngadirPlantillasExercicios,
    Cargando,
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
      cargando: true,
    };
  },
  // cargar exercicios e plantillas ao montar o compoñente
  async mounted() {
    this.cargando = true;
    try {
      await this.cargarExerciciosHoxe();
      await this.cargarPlantillasHoxe();
    } finally {
      this.cargando = false;
      document.addEventListener("click", this.cancelarEdicionAoFora);
    }
  },
  beforeUnmount() {
    // quitar o listener ao desmontar o compoñente
    document.removeEventListener("click", this.cancelarEdicionAoFora);
  },
  methods: {
    // activar a edición dun campo concreto
    activarEdicion(id, campo, valor) {
      this.editando = { id, campo, valor };
      this.$nextTick(() => {
        const input = this.$el.querySelector("input:focus, select:focus");
        if (input) input.focus();
      });
    },

    // gardar un campo editado mediante chamada PATCH
    async guardarCampoEditado(id, campo) {
      const token = useUsuarioStore().token;
      const novoValor = this.editando.valor;
      this.editando = { id: null, campo: null, valor: "" };
      try {
        await fetch(`https://uplife-final.onrender.com/api/exercicios/${id}/`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ [campo]: novoValor }),
        });
        this.cargarExerciciosHoxe();
      } catch (error) {
        console.error("Erro ao actualizar exercicio:", error);
      }
    },

    // cancelar edición se se fai click fóra da celda editable
    cancelarEdicionAoFora(e) {
      const path = e.composedPath?.() || e.path || [];
      const clickedInsideInput = path.some((el) =>
        el?.classList?.contains("editable")
      );
      if (!clickedInsideInput) {
        this.editando = { id: null, campo: null, valor: "" };
      }
    },

    // devolver nome da categoría segundo o seu id
    nomeCategoriaPorId(id) {
      return this.categoriasMap[id] || "Descoñecida";
    },

    // cargar exercicios feitos polo usuario na data actual
    async cargarExerciciosHoxe() {
      const idUsuario = useUsuarioStore().id;
      const token = useUsuarioStore().token;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/exercicios/",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const exercicios = await response.json();
        this.exerciciosHoxe = exercicios
          .filter((ex) => ex.usuario === idUsuario && ex.data === hoxe)
          .sort((a, b) => a.id_exercicio - b.id_exercicio);
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro cargando exercicios:", error);
      }
    },

    // cargar plantillas usadas polo usuario na data actual
    async cargarPlantillasHoxe() {
      const idUsuario = useUsuarioStore().id;
      const token = useUsuarioStore().token;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas-uso/",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const usos = await response.json();

        // filtrar só as plantillas do usuario no día de hoxe
        const usosFiltrados = usos.filter(
          (uso) => uso.usuario === idUsuario && uso.data === hoxe
        );

        // cargar os datos das plantillas asociadas
        const plantillasCompletas = await Promise.all(
          usosFiltrados.map(async (uso) => {
            const plantillaResponse = await fetch(
              `https://uplife-final.onrender.com/api/plantillas/${uso.plantilla}/`,
              {
                headers: { Authorization: `Bearer ${token}` },
              }
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

    // eliminar unha plantilla usada hoxe
    async eliminarPlantilla(id_plantilla) {
      const idUsuario = useUsuarioStore().id;
      const token = useUsuarioStore().token;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas-uso/",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const usos = await response.json();

        // atopar o rexistro de uso correspondente á plantilla de hoxe
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
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        this.cargarPlantillasHoxe();
        this.$refs.historialRef?.cargarExercicios();
      } catch (error) {
        console.error("Erro eliminando plantilla:", error);
      }
    },

    // engadir unha plantilla usada hoxe polo usuario
    async engadirPlantilla(nomePlantilla) {
      const idUsuario = useUsuarioStore().id;
      const token = useUsuarioStore().token;
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas/",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const plantillas = await response.json();
        const plantilla = plantillas.find(
          (p) => p.usuario === idUsuario && p.nome === nomePlantilla
        );

        await fetch("https://uplife-final.onrender.com/api/plantillas-uso/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
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

    // eliminar un exercicio polo seu ID
    async eliminarExercicio(id) {
      const token = useUsuarioStore().token;
      try {
        await fetch(`https://uplife-final.onrender.com/api/exercicios/${id}/`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
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
  <div>
    <Cargando v-if="cargando" />
    <div v-else id="divXeral2">
      <h1 class="titulo">Exercicios</h1>
      <div class="tarxetas">
        <div
          class="tarxeta"
          :class="{ inactiva: componenteActivo !== 'historial' }"
          @click="componenteActivo = 'historial'"
        >
          <a href="#">Historial</a>
        </div>
        <div
          class="tarxeta"
          :class="{ inactiva: componenteActivo !== 'engadirE' }"
          @click="componenteActivo = 'engadirE'"
        >
          <a href="#">Engadir exercicios</a>
        </div>
        <div
          class="tarxeta"
          :class="{ inactiva: componenteActivo !== 'engadirP' }"
          @click="componenteActivo = 'engadirP'"
        >
          <a href="#">Engadir plantillas</a>
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
                      @blur="
                        guardarCampoEditado(exercicio.id_exercicio, 'nome')
                      "
                      @keyup.enter="
                        guardarCampoEditado(exercicio.id_exercicio, 'nome')
                      "
                      @click.stop
                    />
                    <span v-else>{{ exercicio.nome }}</span>
                  </td>

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
                        guardarCampoEditado(
                          exercicio.id_exercicio,
                          'repeticions'
                        )
                      "
                      @keyup.enter="
                        guardarCampoEditado(
                          exercicio.id_exercicio,
                          'repeticions'
                        )
                      "
                      @click.stop
                    />
                    <span v-else>{{ exercicio.repeticions }}</span>
                  </td>

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
                      @blur="
                        guardarCampoEditado(exercicio.id_exercicio, 'peso')
                      "
                      @keyup.enter="
                        guardarCampoEditado(exercicio.id_exercicio, 'peso')
                      "
                      @click.stop
                    />
                    <span v-else>{{ exercicio.peso }} </span>
                  </td>

                  <td>
                    <a href="#">
                      <img
                        src="/imaxes/trash.png"
                        alt="icona borrar"
                        @click="eliminarExercicio(exercicio.id_exercicio)"
                        class="icon2"
                      />
                    </a>
                  </td>
                </tr>
                <tr v-if="exerciciosHoxe.length === 0">
                  <td colspan="4">Non hai exercicios rexistrados para hoxe.</td>
                </tr>
              </tbody>
            </table>
            <button @click="componenteActivo = 'engadirE'">+</button>
          </div>

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
                    <a href="#">
                      <img
                        src="/imaxes/trash.png"
                        alt="icona borrar"
                        @click="eliminarPlantilla(plantilla.id_plantilla)"
                        class="icon"
                      />
                    </a>
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
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  margin-bottom: 1%;
  height: 100%;
  overflow: hidden;
  border-radius: 8px;
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
    overflow: visible !important;
    padding: 1rem;
    box-sizing: border-box;
  }
  .dereita {
    border-radius: 0 0 8px 8px;
  }
  .esquerda {
    border-radius: 0;
  }
  .esquerdaAbaixo {
    width: 100%;
    overflow-x: auto;
    padding: 0;
  }

  .esquerdaArriba {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  table {
    width: 100%;
    min-width: 480px;
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
    font-size: 0.7rem;
    word-break: break-word;
  }

  td {
    background-color: #f9f9f9;
    width: 1.25rem;
    height: 1.25rem;
  }

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

  .tarxetas {
    display: flex;
    width: 100%;
    justify-content: center;
    flex-direction: row;
    width: 82%;
    height: 50px;
    margin-left: 8%;
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
@media (min-width: 769px) and (max-width: 1370px) {
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
    overflow: visible !important;
    padding: 1rem;
    box-sizing: border-box;
  }
  .dereita {
    border-radius: 0 0 8px 8px;
  }
  .esquerda {
    border-radius: 0;
  }
  .esquerdaAbaixo {
    width: 100%;
    overflow-x: auto;
    padding: 0;
  }

  .esquerdaArriba {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  table {
    width: 100%;
    min-width: 480px;
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
    font-size: 0.7rem;
    word-break: break-word;
  }

  td {
    background-color: #f9f9f9;
    width: 1.25rem;
    height: 1.25rem;
  }

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

  .tarxetas {
    display: flex;
    width: 100%;
    justify-content: center;
    flex-direction: row;
    width: 82%;
    height: 50px;
    margin-left: 8%;
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
