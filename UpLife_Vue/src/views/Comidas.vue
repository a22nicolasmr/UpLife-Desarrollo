<script>
import EngadirComida from "@/components/Comidas/EngadirComida.vue";
import GrupoComida from "@/components/Comidas/GrupoComida.vue";
import HistorialComidas from "@/components/Comidas/HistorialComidas.vue";
import TotalComida from "@/components/Comidas/TotalComida.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    EngadirComida,
    GrupoComida,
    HistorialComidas,
    TotalComida,
  },
  data() {
    return {
      componenteActivo: "historial",
      grupos: [],
      expandedGrupos: [],
      grupoSeleccionado: null,
      grupoSeleccionadoMandar: null,
      editando: { id: null, campo: null, valor: "" },
    };
  },
  computed: {
    //cargar id de usuario do store
    idUsuario() {
      return useUsuarioStore().id;
    },

    //cargar calorías do store
    caloriasTotaisNecesarias() {
      return useUsuarioStore().calorias;
    },

    //calcular as calorías inxeridas según o peso es as calorías por 100g dos alimentos
    caloriasInxeridasHoxe() {
      const total = this.grupos.reduce((sum, grupo) => {
        return (
          sum +
          (grupo.comidas || []).reduce((acc, comida) => {
            const caloriasPor100g = comida.calorias || 0;
            const pesoEnGramos = comida.peso || 0;
            const caloriasTotales = (caloriasPor100g / 100) * pesoEnGramos;
            return acc + caloriasTotales;
          }, 0)
        );
      }, 0);
      return Math.ceil(total);
    },

    //calcular porcentaxe das calorías inxeridas
    porcentaxeCalorias() {
      const total = this.caloriasTotaisNecesarias;
      const inxerida = this.caloriasInxeridasHoxe;
      if (!total || total <= 0) return 0;
      return Math.min(Math.round((inxerida / total) * 100), 100);
    },
  },
  //cargar datos cando se monta o compoñente
  mounted() {
    this.cargarDatos();
  },
  methods: {
    //cargar datos dos grupos filtrado por id de usuario e mapeado por comidas
    async cargarDatos() {
      const hoxe = new Date().toISOString().split("T")[0];
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/grupos/"
        );
        if (!response.ok) throw new Error("Erro ao cargar grupos");
        const grupos = await response.json();

        this.grupos = grupos
          .filter((g) => g.usuario === this.idUsuario)
          .map((g) => ({
            ...g,
            comidas: (g.comidas || []).filter((c) => c.data === hoxe),
          }))
          .sort((a, b) => a.id_grupo - b.id_grupo);

        this.componenteActivo = "historial";
      } catch (error) {
        console.error("Erro cargando datos:", error);
      }
    },

    //borrar grupo por id
    async borrarGrupo(id) {
      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/grupos/${id}/`,
          { method: "DELETE" }
        );
        if (!response.ok) throw new Error("Erro ao eliminar grupo");
        this.grupos = this.grupos.filter((g) => g.id_grupo !== id);
        this.componenteActivo = "historial";
        this.$refs.hijoRef.cargarComidas();
        this.$refs.hijoRef.cargarGrupos();
      } catch (error) {
        console.error("Erro eliminando grupo:", error);
      }
    },

    //borrar comida por id
    async borrarComida(idComida) {
      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/comidas/${idComida}/`,
          { method: "DELETE" }
        );
        if (!response.ok) throw new Error("Erro ao eliminar comida");

        this.grupos.forEach((g) => {
          g.comidas = g.comidas.filter((c) => c.id_comida !== idComida);
        });
        this.componenteActivo = "historial";
        this.$refs.hijoRef.cargarComidas();
        this.$refs.hijoRef.cargarGrupos();
      } catch (error) {
        console.error("Erro eliminando comida:", error);
      }
    },

    //expandir ou comprimir grupo por id
    toggleExpand(id) {
      if (this.expandedGrupos.includes(id)) {
        this.expandedGrupos = this.expandedGrupos.filter((gid) => gid !== id);
      } else {
        this.expandedGrupos.push(id);
      }
    },

    //calcular valor por peso
    calcular(valorPor100, peso) {
      if (!valorPor100 || !peso) return 0;
      return ((valorPor100 / 100) * peso).toFixed(1);
    },

    //activar edición de celas por id e campo
    activarEdicion(id, campo) {
      const comida = this.grupos
        .flatMap((g) => g.comidas || [])
        .find((c) => c.id_comida === id);
      if (!comida) return;

      this.editando = { id, campo, valor: comida[campo] };

      //poñer o foco no input unha vez cargado no DOM
      this.$nextTick(() => {
        const input = this.$refs.editInput;
        if (input && input.focus) {
          Array.isArray(input) ? input[0].focus() : input.focus();
        }
      });
    },

    //actualizar elemento editado
    async guardarCampoEditado(id, campo) {
      const novoValor = this.editando.valor;
      this.editando = { id: null, campo: null, valor: "" };
      try {
        await fetch(`https://uplife-final.onrender.com/api/comidas/${id}/`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ [campo]: novoValor }),
        });
        this.cargarDatos();
        this.$refs.hijoRef.cargarGrupos();
        this.$refs.hijoRef.cargarComidas();
      } catch (error) {
        console.error("Erro ao actualizar comida:", error);
      }
    },
  },
};
</script>

<template>
  <div id="divXeral2">
    <h1 class="titulo">Grupos de Comidas</h1>

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
        :class="{ inactiva: componenteActivo !== 'engadirC' }"
        @click="componenteActivo = 'engadirC'"
      >
        Engadir
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'total' }"
        @click="componenteActivo = 'total'"
      >
        Total
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'grupo' }"
        @click="componenteActivo = 'grupo'"
      >
        Grupo
      </div>
    </div>

    <div class="plantilla-layout">
      <div class="esquerda">
        <!-- GRÁFICO DE PROGRESO DE CALORÍAS -->
        <div class="grafico-calorias">
          <svg viewBox="0 0 36 36" class="circular-chart">
            <path
              class="circle-bg"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831
                 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              class="circle"
              :stroke-dasharray="porcentaxeCalorias + ', 100'"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831
                 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <text x="18" y="20.35" class="percentage">
              {{ porcentaxeCalorias }}%
            </text>
          </svg>
          <div class="info-calorias">
            <p>
              <strong>Calorías restantes:</strong>
              {{ caloriasTotaisNecesarias - caloriasInxeridasHoxe }} kcal
            </p>
            <p><strong>Inxeridas:</strong> {{ caloriasInxeridasHoxe }} kcal</p>
          </div>
        </div>

        <div v-for="grupo in grupos" :key="grupo.id_grupo" class="divPlantilla">
          <div class="plantilla-header">
            <img :src="grupo.icona" alt="icona grupo" />
            <h3>{{ grupo.nome }}</h3>
            <div class="botons-container">
              <button
                class="expand-button"
                @click.stop="toggleExpand(grupo.id_grupo)"
                :class="{
                  rotated: expandedGrupos.includes(grupo.id_grupo),
                }"
              >
                ▼
              </button>
              <button
                class="button-add"
                @click="
                  componenteActivo = 'engadirC';
                  grupoSeleccionado = grupo.id_grupo;
                  grupoSeleccionadoMandar = grupo.id_grupo;
                "
              >
                +
              </button>
              <img
                src="/imaxes/trash.png"
                alt="icona borrar"
                class="icono-trash"
                @click="borrarGrupo(grupo.id_grupo)"
              />
            </div>
          </div>

          <transition name="fade-slide">
            <div
              v-if="expandedGrupos.includes(grupo.id_grupo)"
              class="exercicios-plantilla"
            >
              <template v-if="grupo.comidas && grupo.comidas.length">
                <table class="tabela-exercicios">
                  <thead>
                    <tr>
                      <th>Nome</th>
                      <th>Peso (g)</th>
                      <th>Calorías</th>
                      <th>Carbohidratos (g)</th>
                      <th>Proteínas (g)</th>
                      <th>Graxas (g)</th>
                      <th>Eliminar</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="comida in grupo.comidas" :key="comida.id_comida">
                      <td @click="activarEdicion(comida.id_comida, 'nome')">
                        <input
                          ref="editInput"
                          v-if="
                            editando.id === comida.id_comida &&
                            editando.campo === 'nome'
                          "
                          v-model="editando.valor"
                          @blur="guardarCampoEditado(comida.id_comida, 'nome')"
                          @keyup.enter="
                            guardarCampoEditado(comida.id_comida, 'nome')
                          "
                          @click.stop
                        />

                        <span v-else>{{ comida.nome }}</span>
                      </td>
                      <td @click="activarEdicion(comida.id_comida, 'peso')">
                        <input
                          ref="editInput"
                          v-if="
                            editando.id === comida.id_comida &&
                            editando.campo === 'peso'
                          "
                          type="number"
                          v-model.number="editando.valor"
                          @blur="guardarCampoEditado(comida.id_comida, 'peso')"
                          @keyup.enter="
                            guardarCampoEditado(comida.id_comida, 'peso')
                          "
                          @click.stop
                        />

                        <span v-else>{{ comida.peso }}</span>
                      </td>
                      <td>{{ calcular(comida.calorias, comida.peso) }} kcal</td>
                      <td>
                        {{ calcular(comida.carbohidratos, comida.peso) }} g
                      </td>
                      <td>{{ calcular(comida.proteinas, comida.peso) }} g</td>
                      <td>{{ calcular(comida.graxas, comida.peso) }} g</td>
                      <td>
                        <img
                          src="/imaxes/trash.png"
                          alt="borrar comida"
                          class="icono-borrar-ex"
                          @click="borrarComida(comida.id_comida)"
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
              </template>
              <p v-else class="sen-exercicios">Este grupo non ten comidas.</p>
            </div>
          </transition>
        </div>
        <button @click="componenteActivo = 'engadirC'" id="engadirE">+</button>
      </div>

      <div class="dereita">
        <HistorialComidas
          v-if="componenteActivo === 'historial'"
          @cargarDatos="cargarDatos"
          ref="hijoRef"
        />
        <EngadirComida
          v-if="componenteActivo === 'engadirC'"
          :grupoSeleccionadoMandar="grupoSeleccionadoMandar"
          @cargarDatos="cargarDatos"
        />
        <TotalComida v-if="componenteActivo === 'total'" />
        <GrupoComida
          v-if="componenteActivo === 'grupo'"
          @cargarDatos="cargarDatos"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Gráfico circular */
.grafico-calorias {
  display: flex;
  align-items: center;
  gap: 5%;
  justify-content: left;
  margin-bottom: 3%;
}
.circular-chart {
  max-width: 15%;
  max-height: 15%;
}
.circle-bg {
  fill: none;
  stroke: #eee;
  stroke-width: 3.8;
}
.circle {
  fill: none;
  stroke: rgba(255, 0, 0, 0.753);
  stroke-width: 3.8;
  stroke-linecap: round;
  transform: rotate(-90deg);
  transform-origin: center;
  transition: stroke-dasharray 0.5s;
}
.percentage {
  fill: rgba(255, 0, 0, 0.753);
  font-size: x-small;
  text-anchor: middle;
}
.info-calorias p {
  margin: 2px 0;
  color: #666;
  font-size: large;
}

/* Resto de estilos ya existentes... */
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
  height: 100vh;

  margin-bottom: 2%;
  overflow: hidden;
}

.titulo {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
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
  flex-grow: 1;
  /* height: calc(100vh - 30vh); */
  height: 100%;
  overflow: hidden;
  margin-bottom: 2%;
}

.esquerda {
  width: 60%;
  padding: 2%;
  box-sizing: border-box;
  height: 100%;
  overflow-y: auto;
}

.dereita {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  overflow-y: auto;
  box-sizing: border-box;
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
  width: 25%;
  height: 25%;
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
  margin: 0;
}

.icono-trash {
  width: 18%;
  height: 18%;
  cursor: pointer;
  margin-top: 30%;
}
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

.tabela-exercicios input {
  width: 100%;
  border: none;
  outline: none;
  text-align: center;
  padding: 4px;
  font-size: medium;
}

.tabela-exercicios input:focus {
  outline: 2px solid #7f5af0;
  border-radius: 4px;
}

.tabela-exercicios select {
  width: 100%;
  border: none;
  outline: none;
  text-align: center;
  font-size: medium;
}

.tabela-exercicios select:focus {
  outline: 2px solid #7f5af0;
  border-radius: 4px;
}
@media (max-width: 768px) {
  .plantilla-layout {
    flex-direction: column;
    height: auto;
    width: 100%;
    overflow: visible;
    margin: 0;
  }

  .esquerda,
  .dereita {
    width: 100%;
    height: auto;
    padding: 1rem;
    box-sizing: border-box;
    overflow: visible;
  }

  .grafico-calorias {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1rem;
  }

  .circular-chart {
    max-width: 40%;
    max-height: 40%;
  }

  .info-calorias p {
    font-size: 1rem;
  }

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

  .tabela-exercicios {
    min-width: 600px;
    font-size: 0.85rem;
  }

  .exercicios-plantilla {
    overflow-x: auto;
  }

  .button-add {
    font-size: 1.5rem;
    padding: 0.5rem 1rem;
  }

  .icono-trash {
    width: 1.2rem;
    height: 1.2rem;
    margin-top: 0;
  }

  .expand-button {
    font-size: 1.2rem;
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
  #divXeral2 {
    height: auto;
    overflow-y: auto;
    padding-bottom: 2rem; /* espacio para evitar recorte inferior */
  }

  body {
    overflow-x: hidden;
  }
  .icono-trash {
    margin-top: 15%;
    margin-right: 5%;
  }
}
</style>
