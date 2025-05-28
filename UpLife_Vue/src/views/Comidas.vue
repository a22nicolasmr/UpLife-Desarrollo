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
    // obter o id do usuario desde o store
    idUsuario() {
      return useUsuarioStore().id;
    },
    // obter as calorías necesarias desde o store
    caloriasTotaisNecesarias() {
      return useUsuarioStore().calorias;
    },
    // calcular as calorías inxeridas polo usuario no día actual
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
    // calcular a porcentaxe de calorías consumidas
    porcentaxeCalorias() {
      const total = this.caloriasTotaisNecesarias;
      const inxerida = this.caloriasInxeridasHoxe;
      if (!total || total <= 0) return 0;
      return Math.min(Math.round((inxerida / total) * 100), 100);
    },
    // calcular as calorías restantes para chegar ao obxectivo
    caloriasRestantes() {
      const necesarias = this.caloriasTotaisNecesarias;
      const inxeridas = this.caloriasInxeridasHoxe;
      if (!necesarias || necesarias <= 0) return 0;
      const restantes = necesarias - inxeridas;
      return restantes > 0 ? restantes : 0;
    },
  },
  async mounted() {
    // cargar datos ao montar o compoñente
    await this.asegurarDatosUsuarioCargados();
    this.cargarDatos();
  },
  methods: {
    async asegurarDatosUsuarioCargados() {
      const store = useUsuarioStore();
      if (!store.calorias) {
        store.cargarToken();
        const token = store.token;
        try {
          const response = await fetch(
            `https://uplife-final.onrender.com/api/usuarios/${this.idUsuario}/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          const data = await response.json();
          store.nome = data.nome;
          store.altura = data.altura;
          store.peso = data.peso;
          store.xenero = data.xenero;
          store.obxectivo = data.obxectivo;
          store.actividade = data.actividade;
          store.idade = data.idade;
          store.calorias = data.calorias_diarias;
          store.auga = data.auga_diaria;
        } catch (e) {
          console.error("Erro cargando datos do usuario:", e);
        }
      }
    },
    // cargar os grupos de comida do usuario e filtrar as comidas de hoxe
    async cargarDatos() {
      const hoxe = new Date().toISOString().split("T")[0];
      const usuarioStore = useUsuarioStore();
      usuarioStore.cargarToken();
      const token = usuarioStore.token;

      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/grupos/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
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

    // eliminar un grupo e todas as comidas asociadas a ese grupo
    async borrarGrupo(id) {
      const usuarioStore = useUsuarioStore();
      usuarioStore.cargarToken();
      const token = usuarioStore.token;

      try {
        const grupo = this.grupos.find((g) => g.id_grupo === id);
        if (!grupo) throw new Error("Grupo no encontrado");

        const comidas = grupo.comidas || [];
        // eliminar todas as comidas dentro do grupo
        for (const comida of comidas) {
          const res = await fetch(
            `https://uplife-final.onrender.com/api/comidas/${comida.id_comida}/`,
            {
              method: "DELETE",
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          if (!res.ok)
            throw new Error(`Error al eliminar comida ${comida.id_comida}`);
        }

        // eliminar o grupo unha vez eliminadas as comidas
        const response = await fetch(
          `https://uplife-final.onrender.com/api/grupos/${id}/`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (!response.ok) throw new Error("Erro ao eliminar grupo");

        this.grupos = this.grupos.filter((g) => g.id_grupo !== id);
        this.componenteActivo = "historial";
        this.$refs.hijoRef.cargarComidas();
        this.$refs.hijoRef.cargarGrupos();
      } catch (error) {
        console.error("Erro eliminando grupo e comidas:", error);
      }
    },

    // eliminar unha comida concreta polo seu ID
    async borrarComida(idComida) {
      const usuarioStore = useUsuarioStore();
      usuarioStore.cargarToken();
      const token = usuarioStore.token;

      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/comidas/${idComida}/`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
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

    // expandir ou contraer visualmente un grupo
    toggleExpand(id) {
      if (this.expandedGrupos.includes(id)) {
        this.expandedGrupos = this.expandedGrupos.filter((gid) => gid !== id);
      } else {
        this.expandedGrupos.push(id);
      }
    },

    // calcular valor total dun nutriente segundo peso
    calcular(valorPor100, peso) {
      if (!valorPor100 || !peso) return 0;
      return ((valorPor100 / 100) * peso).toFixed(1);
    },

    // activar modo edición para un campo concreto dunha comida
    activarEdicion(id, campo) {
      const comida = this.grupos
        .flatMap((g) => g.comidas || [])
        .find((c) => c.id_comida === id);
      if (!comida) return;

      this.editando = { id, campo, valor: comida[campo] };

      this.$nextTick(() => {
        const input = this.$refs.editInput;
        if (input && input.focus) {
          Array.isArray(input) ? input[0].focus() : input.focus();
        }
      });
    },

    // gardar un campo editado dunha comida mediante PATCH
    async guardarCampoEditado(id, campo) {
      const usuarioStore = useUsuarioStore();
      usuarioStore.cargarToken();
      const token = usuarioStore.token;

      const novoValor = this.editando.valor;
      this.editando = { id: null, campo: null, valor: "" };
      try {
        await fetch(`https://uplife-final.onrender.com/api/comidas/${id}/`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
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
              {{ caloriasRestantes }} kcal
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
          @toggleExpand="toggleExpand"
        />
        <EngadirComida
          v-if="componenteActivo === 'engadirC'"
          :grupoSeleccionadoMandar="grupoSeleccionadoMandar"
          @cargarDatos="cargarDatos"
          @toggleExpand="toggleExpand"
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
  margin-top: 21%;
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
@media (min-width: 769px) and (max-width: 1370px) {
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
