<script>
import { useUsuarioStore } from "@/stores/useUsuario";
import Cargando from "@/components/BarrasNavegacion/Cargando.vue";

export default {
  components: {
    Cargando,
  },
  data() {
    return {
      comidasPorDia: {},
      gruposUsuario: [],
      gruposSeleccionadosPorComida: {},
      error: "",
      cargando: true,
    };
  },
  computed: {
    // obter id do usuario desde o store
    idUsuario() {
      const store = useUsuarioStore();
      return store.id;
    },
    // obter data de hoxe en formato ISO
    dataHoxeISO() {
      return new Date().toLocaleDateString("en-CA");
    },
    // obter token de sesión desde o store
    token() {
      return useUsuarioStore().token;
    },
  },
  async mounted() {
    // cagar grupos e comidas cando se monta o compoñente
    try {
      await this.cargarComidas();
      await this.cargarGrupos();
    } finally {
      this.cargando = false;
    }
  },
  methods: {
    // cargar comidas dos últimos 7 días filtradas por id de usuario e agrupadas por data
    async cargarComidas() {
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/comidas/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        if (!response.ok) throw new Error("Erro ao cargar comidas");

        const comidas = await response.json();

        const seteDiasAtras = new Date();
        seteDiasAtras.setDate(seteDiasAtras.getDate() - 7);
        const seteDiasISO = seteDiasAtras.toISOString().split("T")[0];

        const comidasPorUsuario = comidas.filter(
          (c) => c.usuario === this.idUsuario && c.data >= seteDiasISO
        );

        const agrupados = {};
        comidasPorUsuario.forEach((c) => {
          if (!agrupados[c.data]) agrupados[c.data] = [];
          agrupados[c.data].push(c);
        });

        const comidasOrdenadas = Object.fromEntries(
          Object.entries(agrupados).sort(
            (a, b) => new Date(b[0]) - new Date(a[0])
          )
        );
        this.comidasPorDia = comidasOrdenadas;
      } catch (error) {
        console.error("Erro ao obter historial de comidas:", error);
      }
    },
    // cargar grupos dos últimos 7 días filtrados por id de usuario
    async cargarGrupos() {
      try {
        const response2 = await fetch(
          "https://uplife-final.onrender.com/api/grupos/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const grupos = await response2.json();

        const gruposPorUsuario = grupos.filter(
          (g) => g.usuario === this.idUsuario
        );

        this.gruposUsuario = gruposPorUsuario;
      } catch (error) {
        console.error("Erro ao obter grupos:", error);
      }
    },
    // engadir nova comida ao grupo correspondente
    async engadirComida(comida) {
      this.error = "";
      const grupoSeleccionado =
        this.gruposSeleccionadosPorComida[comida.id_comida];

      if (grupoSeleccionado) {
        const payload = {
          nome: comida.nome,
          peso: comida.peso,
          graxas: comida.graxas,
          carbohidratos: comida.carbohidratos,
          proteinas: comida.proteinas,
          calorias: comida.calorias,
          data: this.dataHoxeISO,
          usuario: this.idUsuario,
        };

        try {
          const response = await fetch(
            "https://uplife-final.onrender.com/api/comidas/",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.token}`,
              },
              body: JSON.stringify(payload),
            }
          );

          if (!response.ok) throw new Error("Erro ao engadir comida");

          const novaComida = await response.json();

          const grupo = this.gruposUsuario.find(
            (g) => g.id_grupo === grupoSeleccionado
          );

          if (!grupo) throw new Error("Grupo non atopado");

          const comidasExistentes = (grupo.comidas || []).map((c) =>
            typeof c === "object" ? c.id_comida : c
          );
          const comidasActualizadas = [
            ...comidasExistentes,
            novaComida.id_comida,
          ];

          const patchResponse = await fetch(
            `https://uplife-final.onrender.com/api/grupos/${grupo.id_grupo}/`,
            {
              method: "PATCH",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.token}`,
              },
              body: JSON.stringify({ comidas: comidasActualizadas }),
            }
          );

          if (!patchResponse.ok) throw new Error("Erro ao actualizar grupo");

          this.$emit("toggleExpand", grupo.id_grupo);

          // cargar datos en Comidas
          this.$emit("cargarDatos");

          // volver a cargar comidas e grupos tras a actualización
          this.cargarComidas();
          this.cargarGrupos();
          this.gruposSeleccionadosPorComida = [];
        } catch (error) {
          console.error("❗Erro no try-catch:", error);
          this.error = "Produciuse un erro ao engadir a comida ao grupo.";
        }
      } else {
        this.error = "Debes indicar unha opción para engadir a comida";
      }
    },
  },
};
</script>

<template>
  <div>
    <Cargando v-if="cargando"></Cargando>
    <div v-else id="divXeral">
      <h2>Historial</h2>
      <div class="historial-scroll">
        <p v-if="Object.keys(comidasPorDia).length === 0" id="aviso">
          Non hai comidas rexistradas
        </p>

        <div
          v-for="(comidas, data) in comidasPorDia"
          :key="data"
          class="grupo-dia"
        >
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
            <li v-for="comida in comidas" :key="comida.id_comida">
              <div class="fila-exercicio">
                <span style="flex: 1">
                  {{ comida.nome }} - {{ comida.peso }}g -
                  {{ Math.ceil((comida.calorias / 100) * comida.peso) }} kcal
                </span>
                <div style="display: flex; gap: 0.5rem; align-items: center">
                  <select
                    class="select-pequeno"
                    v-model="gruposSeleccionadosPorComida[comida.id_comida]"
                  >
                    <option value="">Selecciona un grupo</option>
                    <option
                      v-for="grupo in gruposUsuario"
                      :key="grupo.id_grupo"
                      :value="grupo.id_grupo"
                    >
                      {{ grupo.nome }}
                    </option>
                  </select>

                  <button class="boton-dereita" @click="engadirComida(comida)">
                    +
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <span class="error">{{ error }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.select-pequeno {
  padding: 4px 8px;
  font-size: small;
  border-radius: 6px;
  border: 1px solid #ccc;
}

input,
select {
  padding: 2%;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: medium;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 5%;
}
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

.fila-exercicio {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.boton-dereita {
  background-color: #7f5af0;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.3s ease;
  margin-bottom: 5%;
}

.boton-dereita:hover {
  background-color: #6e4bd9;
}

.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}
</style>
