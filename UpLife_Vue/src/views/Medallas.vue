<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  props: {
    valorMedallas: Array,
  },
  data() {
    return {
      medallas: [],
      primeirasMedallas: [],
      segundasMedallas: [],
      terceirasMedallas: [],
    };
  },
  watch: {
    valorMedallas: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.actualizarMedallas();
        }
      },
      immediate: true,
      deep: true,
    },
  },

  computed: {
    usuarioId() {
      const store = useUsuarioStore();
      return store.id;
    },
  },
  mounted() {
    this.obterMedallas();
  },
  methods: {
    async actualizarMedallas() {
      if (!this.valorMedallas || this.valorMedallas.length === 0) return;

      const usuarioId = this.usuarioId;

      for (const medalla of this.valorMedallas) {
        try {
          const res = await fetch(
            `http://localhost:8001/api/medallas/${medalla.id_medalla}/`
          );
          if (!res.ok) throw new Error("Erro ao obter medalla");

          const medallaActual = await res.json();

          const xaIncluido = medallaActual.usuarios.includes(usuarioId);

          // ⚠️ Solo actualizar se está completada e o usuario non está xa asignado
          if (medalla.completado && !xaIncluido) {
            await fetch(
              `http://localhost:8001/api/medallas/${medalla.id_medalla}/`,
              {
                method: "PATCH",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  completado: true,
                  usuarios: [...medallaActual.usuarios, usuarioId],
                }),
              }
            );
          }
        } catch (error) {
          console.error(
            `Erro ao actualizar medalla ${medalla.id_medalla}`,
            error
          );
        }
      }

      await this.obterMedallas();
      useUsuarioStore().updateNumeroMedallas();
    },
    //obter medallas
    async obterMedallas() {
      try {
        const response = await fetch("http://localhost:8001/api/medallas/");
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
        console.error("Error cargando datos de medallas:", error);
      }
    },

    //obter medallas completadas polo usuario
    medallaCompletadaPorUsuario(medalla) {
      return medalla.usuarios.includes(this.usuarioId) && medalla.completado;
    },
  },
};
</script>

<template>
  <div id="todo">
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
                <img :src="medalla.icona" alt="Icona medalla" />
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
                <img :src="medalla.icona" alt="Icona medalla" />
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
                <img :src="medalla.icona" alt="Icona medalla" />
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
</template>

<style scoped>
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
</style>
