<script>
import { useUsuarioStore } from "@/stores/useUsuario";

import Cargando from "@/components/BarrasNavegacion/Cargando.vue";

export default {
  components: {
    Cargando,
  },
  props: {
    valorMedallas: Array,
  },
  data() {
    return {
      medallas: [],
      primeirasMedallas: [],
      segundasMedallas: [],
      terceirasMedallas: [],
      cargando: true,
    };
  },
  async mounted() {
    try {
      await this.obterMedallas();
    } finally {
      this.cargando = false;
    }
  },

  watch: {
    // actualizar e obter medallas se o valor da variable valorMedallas cambia
    valorMedallas: {
      async handler(newVal) {
        if (newVal && newVal.length > 0) {
          await this.actualizarMedallas();
          await this.obterMedallas();
        }
      },
      immediate: true,
      deep: true,
    },
  },

  computed: {
    // variables globais do id de usuario e do token
    usuarioId() {
      return useUsuarioStore().id;
    },
    token() {
      return useUsuarioStore().token;
    },
  },

  methods: {
    // actualizar valores das medallas
    async actualizarMedallas() {
      if (!this.valorMedallas || this.valorMedallas.length === 0) return;

      const usuarioId = this.usuarioId;
      const token = this.token;
      let algunhaActualizada = false;

      for (const medalla of this.valorMedallas) {
        try {
          const res = await fetch(
            `https://uplife-final.onrender.com/api/medallas/${medalla.id_medalla}/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          if (!res.ok) throw new Error("Erro ao obter medalla");

          const medallaActual = await res.json();
          const xaIncluido =
            medallaActual.usuarios.includes(usuarioId) &&
            medallaActual.completado;

          // actualizar a medalla como completada no servidor se está completada
          if (medalla.completado && !xaIncluido) {
            const patchRes = await fetch(
              `https://uplife-final.onrender.com/api/medallas/${medalla.id_medalla}/`,
              {
                method: "PATCH",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                  completado: true,
                  usuarios: [...medallaActual.usuarios, usuarioId],
                }),
              }
            );

            if (!patchRes.ok) {
              throw new Error(
                `PATCH fallou para medalla ${medalla.id_medalla}`
              );
            }

            algunhaActualizada = true;
          }
        } catch (error) {
          console.error(
            `❌ Erro ao actualizar medalla ${medalla.id_medalla}:`,
            error
          );
        }
      }

      if (algunhaActualizada) {
        await this.obterMedallas();
        this.$emit("medallasActualizadas");
      }
    },

    // obter medallas obtidas polo usuario
    async obterMedallas() {
      const token = this.token;
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/medallas/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        const medallas = await response.json();

        if (medallas) {
          this.medallas = medallas.sort((a, b) => a.id_medalla - b.id_medalla);

          const total = medallas.length;
          const tercio = Math.ceil(total / 3);
          this.primeirasMedallas = medallas.slice(0, tercio);
          this.segundasMedallas = medallas.slice(tercio, tercio * 2);
          this.terceirasMedallas = medallas.slice(tercio * 2, total);
        }
      } catch (error) {
        console.error("❌ Error cargando datos de medallas:", error);
      }
    },

    //comprobar se a medalla está completada
    medallaCompletadaPorUsuario(medalla) {
      return medalla.completado && medalla.usuarios.includes(this.usuarioId);
    },
  },
};
</script>

<template>
  <div>
    <Cargando v-if="cargando" />
    <div v-else id="todo">
      <h1>Medallas</h1>
      <div class="general">
        <div class="medallas-container">
          <div class="column">
            <div
              v-for="medalla in primeirasMedallas"
              :key="medalla.id_medalla"
              class="medalla"
            >
              <div class="medalla-content">
                <div
                  v-if="medallaCompletadaPorUsuario(medalla)"
                  class="check-icon"
                >
                  <img src="/imaxes/check.png" alt="Check" id="check" />
                </div>
                <div v-else>
                  <img
                    src="/imaxes/invisible.PNG"
                    alt="Invisible"
                    id="invisible"
                  />
                </div>
                <div class="medalla-info">
                  <img
                    :src="
                      'https://res.cloudinary.com/dkujevuxh/' + medalla.icona
                    "
                    alt="Icona medalla"
                    id="imaxeMedalla"
                  />
                  <div>
                    <h3>{{ medalla.nome }}</h3>
                    <p>{{ medalla.descripcion }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="column">
            <div
              v-for="medalla in segundasMedallas"
              :key="medalla.id_medalla"
              class="medalla"
            >
              <div class="medalla-content">
                <div
                  v-if="medallaCompletadaPorUsuario(medalla)"
                  class="check-icon"
                >
                  <img src="/imaxes/check.png" alt="Check" id="check" />
                </div>
                <div v-else>
                  <img
                    src="/imaxes/invisible.PNG"
                    alt="Invisible"
                    id="invisible"
                  />
                </div>
                <div class="medalla-info">
                  <img
                    :src="
                      'https://res.cloudinary.com/dkujevuxh/' + medalla.icona
                    "
                    alt="Icona medalla"
                    id="imaxeMedalla2"
                  />
                  <div>
                    <h3>{{ medalla.nome }}</h3>
                    <p>{{ medalla.descripcion }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="column">
            <div
              v-for="medalla in terceirasMedallas"
              :key="medalla.id_medalla"
              class="medalla"
            >
              <div class="medalla-content">
                <div
                  v-if="medallaCompletadaPorUsuario(medalla)"
                  class="check-icon"
                >
                  <img src="/imaxes/check.png" alt="Check" id="check" />
                </div>
                <div v-else>
                  <img
                    src="/imaxes/invisible.PNG"
                    alt="Invisible"
                    id="invisible"
                  />
                </div>
                <div class="medalla-info">
                  <img
                    :src="
                      'https://res.cloudinary.com/dkujevuxh/' + medalla.icona
                    "
                    alt="Icona medalla"
                    id="imaxeMedalla3"
                  />
                  <div>
                    <h3>{{ medalla.nome }}</h3>
                    <p>{{ medalla.descripcion }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#imaxeMedalla3,
#imaxeMedalla2,
#imaxeMedalla {
  background-color: white;
}

.general {
  width: 93%;
  padding: 3%;
  box-sizing: border-box;
  background-color: white;
  border-radius: 1vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2%;
}

.medallas-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2vw;
  width: 100%;
  justify-content: center;
}

.column {
  flex: 1 1 30%;
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.medalla {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #f7f7f7;
  border-radius: 1vw;
  padding: 1vh 1vw;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  height: 13.5vh;
  box-sizing: border-box;
}

.medalla-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 1vw;
  height: 100%;
}

.check-icon,
#invisible {
  width: 2vh;
  height: 2vh;
  margin-left: 0.5vw;
  flex-shrink: 0;
}

.medalla-info {
  display: flex;
  align-items: center;
  gap: 1vw;
  flex-grow: 1;
}

.medalla-info img {
  width: 4.5vw;
  height: 4.5vw;
  object-fit: cover;
  border-radius: 10%;
  flex-shrink: 0;
}

.medalla-info div {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

img {
  max-width: 100%;
  border-radius: 8%;
}

h1 {
  font-size: xx-large;
  margin-bottom: 2%;
  color: #7f5af0;
}

h3 {
  font-size: 1.2vw;
  margin: 0;
  color: #333;
}

p {
  font-size: 1vw;
  margin: 0;
  color: #666;
}

#todo {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}
@media (max-width: 768px) {
  .medallas-container {
    flex-direction: column;
    gap: 1rem;
    align-items: center;
  }
  .general {
    width: 100%;
  }
  .column {
    flex: 1 1 100%;
    width: 100%;
    max-width: 100%;
  }

  .medalla {
    height: auto;
    padding: 1rem;
  }

  .medalla-info img {
    width: 20vw;
    height: 20vw;
  }

  h3 {
    font-size: 1rem;
  }

  p {
    font-size: 0.9rem;
  }

  .check-icon,
  #invisible {
    width: 3vh;
    height: 3vh;
  }
}

@media (min-width: 769px) and (max-width: 1370px) {
  .medallas-container {
    flex-direction: column;
    gap: 1rem;
    align-items: center;
  }
  .general {
    width: 100%;
  }
  .column {
    flex: 1 1 100%;
    width: 100%;
    max-width: 100%;
  }

  .medalla {
    height: auto;
    padding: 1rem;
  }

  .medalla-info img {
    width: 20vw;
    height: 20vw;
  }

  h3 {
    font-size: 1rem;
  }

  p {
    font-size: 0.9rem;
  }

  .check-icon,
  #invisible {
    width: 3vh;
    height: 3vh;
  }
}
</style>
