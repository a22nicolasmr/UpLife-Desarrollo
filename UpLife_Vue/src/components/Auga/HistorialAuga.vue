<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      augaPorDia: {},
    };
  },
  computed: {
    // obter id de usuario do store
    idUsuario() {
      return useUsuarioStore().id;
    },

    // obter a data de hoxe en formato ISO
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },

    // obter a auga diaria establecida polo usuario
    augaUsuario() {
      return useUsuarioStore().auga;
    },

    // obter o token do usuario
    token() {
      return useUsuarioStore().token;
    },
  },
  async mounted() {
    // cargar rexistros de auga ao montar o compoñente
    this.cargarAuga();
  },

  methods: {
    // cargar rexistros de auga filtrados por usuario e últimos 7 días
    async cargarAuga() {
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/auga/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        if (!response.ok) throw new Error("Erro ao cargar auga");

        const auga = await response.json();
        const augaPorUsuario = auga.filter((a) => a.usuario === this.idUsuario);
        const seteDiasAtras = new Date();
        seteDiasAtras.setDate(seteDiasAtras.getDate() - 7);

        const augaFiltrados = augaPorUsuario.filter((a) => {
          const dataAuga = new Date(a.data);
          return dataAuga >= seteDiasAtras;
        });

        const agrupados = {};
        augaFiltrados.forEach((a) => {
          if (!agrupados[a.data]) agrupados[a.data] = [];
          agrupados[a.data].push(a);
        });

        this.augaPorDia = Object.fromEntries(
          Object.entries(agrupados).sort(
            (a, b) => new Date(b[0]) - new Date(a[0])
          )
        );
      } catch (error) {
        console.error("Erro ao obter historial:", error);
      }
    },

    // engadir novo rexistro de auga
    async engadirAuga(auga) {
      const payload = {
        cantidade: auga.cantidade,
        hora: auga.hora,
        data: this.dataHoxeISO,
        usuario: this.idUsuario,
      };

      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/auga/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) {
          throw new Error("Erro ao engadir auga");
        }

        await response.json();
        this.$emit("cargarAugaHoxe");
      } catch (error) {
        console.error("❗Erro no try-catch:", error);
      }
    },
  },
};
</script>

<template>
  <div id="divXeral">
    <h2>Historial de auga</h2>
    <p v-if="Object.keys(augaPorDia).length === 0" id="aviso">
      Non hai auga rexistrada
    </p>
    <div class="historial-scroll">
      <div v-for="(augas, data) in augaPorDia" :key="data" class="grupo-dia">
        <h3>
          {{
            new Date(data).toLocaleDateString("gl-ES", {
              weekday: "long",
              day: "numeric",
              month: "long",
            })
          }}
        </h3>
        <ul>
          <li v-for="auga in augas" :key="auga.id_auga">
            <div class="fila-auga">
              <span
                >Hora
                {{
                  new Date("1970-01-01T" + auga.hora + "Z").toLocaleTimeString(
                    "gl-ES",
                    { hour: "2-digit", minute: "2-digit" }
                  )
                }}
                - {{ auga.cantidade }} ml
              </span>
              <button class="boton-dereita" @click="engadirAuga(auga)">
                +
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
#divXeral {
  padding: 5%;
}

h2 {
  color: #7f5af0;
  margin-bottom: 2%;
}

.historial-scroll {
  overflow-y: auto;
  padding-right: 2%;
}

.grupo-dia {
  border-bottom: 1px solid #aaa;
  padding-bottom: 2%;
}

h3 {
  color: white;
  margin-bottom: 5px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  color: white;
  padding: 1% 0;
}

.fila-auga {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.boton-dereita {
  background-color: #7f5af0;
  color: white;
  border: none;
  padding: 1% 2%;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.3s ease;
}

.boton-dereita:hover {
  background-color: #6e4bd9;
}
</style>
