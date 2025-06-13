<script>
import { useUsuarioStore } from "@/stores/useUsuario";
import Cargando from "@/components/BarrasNavegacion/Cargando.vue";

export default {
  components: {
    Cargando,
  },
  data() {
    return {
      exerciciosPorDia: {},
      actividadesPorDia: {},
      plantillasUsuario: [],
      plantillaSeleccionada: {},
      erro: "",
      cargando: true,
    };
  },
  computed: {
    // obter id do usuario desde o store
    idUsuario() {
      return useUsuarioStore().id;
    },
    // obter token do usuario desde o store
    token() {
      return useUsuarioStore().token;
    },
    // obter data de hoxe en formato ISO
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
  },
  async mounted() {
    // cargar plantillas e exercicios ao montar o compoñente
    try {
      await this.cargarPlantillasUsuario();
      await this.cargarExercicios();
    } finally {
      this.cargando = false;
    }
  },
  methods: {
    // validar formulario
    comprobarErro(idExercicio) {
      if (!this.plantillaSeleccionada[idExercicio]) {
        this.erro = "Completa todos os campos";
        return true;
      }
      this.erro = ""; // limpiamos si todo está correcto
      return false;
    },
    // cargar plantillas do usuario
    async cargarPlantillasUsuario() {
      try {
        const res = await fetch(
          "https://uplife-final.onrender.com/api/plantillas/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const data = await res.json();
        this.plantillasUsuario = data.filter(
          (p) => p.usuario === this.idUsuario
        );
      } catch (error) {
        console.error("Erro ao cargar plantillas:", error);
      }
    },

    // cargar exercicios  dos últimos 7 días
    async cargarExercicios() {
      try {
        const [resEx] = await Promise.all([
          fetch("https://uplife-final.onrender.com/api/exercicios/", {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }),
        ]);

        if (!resEx.ok) throw new Error("Erro ao cargar datos");

        const exercicios = await resEx.json();

        const seteDiasAtras = new Date();
        seteDiasAtras.setDate(seteDiasAtras.getDate() - 7);
        const seteDiasAtrasISO = seteDiasAtras.toISOString().split("T")[0];

        const userId = this.idUsuario;

        const exerciciosFiltrados = exercicios.filter(
          (e) => e.usuario === userId && e.data >= seteDiasAtrasISO
        );

        const actividades = {};

        exerciciosFiltrados.forEach((ex) => {
          if (!actividades[ex.data])
            actividades[ex.data] = { exercicios: [], plantillas: [] };
          actividades[ex.data].exercicios.push(ex);
        });

        this.actividadesPorDia = Object.fromEntries(
          Object.entries(actividades).sort(
            (a, b) => new Date(b[0]) - new Date(a[0])
          )
        );
      } catch (error) {
        console.error("Erro ao obter historial:", error);
      }
    },

    // engadir novo exercicio
    async engadirExercicio(exercicio) {
      const payload = {
        nome: exercicio.nome,
        repeticions: exercicio.repeticions,
        peso: exercicio.peso,
        data: this.dataHoxeISO,
        usuario: this.idUsuario,
        categoria: exercicio.categoria,
      };
      try {
        const res = await fetch(
          "https://uplife-final.onrender.com/api/exercicios/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify(payload),
          }
        );
        if (!res.ok) throw new Error("Erro ao engadir exercicio");
        this.$emit("cargarExerciciosHoxe");
      } catch (error) {
        console.error("❗Erro ao engadir exercicio:", error);
      }
    },

    // engadir exercicio a unha plantilla
    async engadirExercicioAPlantilla(exercicio, idPlantilla) {
      this.erro = "";
      if (this.comprobarErro(exercicio.id_exercicio)) return;
      try {
        const plantillaRes = await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${idPlantilla}/`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        if (!plantillaRes.ok)
          throw new Error("Non se puido cargar a plantilla");

        const plantilla = await plantillaRes.json();
        const idsExerciciosExistentes = plantilla.exercicios.map((e) =>
          typeof e === "object" ? e.id_exercicio : e
        );

        if (!idsExerciciosExistentes.includes(exercicio.id_exercicio)) {
          idsExerciciosExistentes.push(exercicio.id_exercicio);
        }

        const patchRes = await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${idPlantilla}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify({
              exercicios: idsExerciciosExistentes,
            }),
          }
        );

        if (!patchRes.ok)
          throw new Error("Erro ao engadir exercicio á plantilla");

        this.plantillaSeleccionada = {};
        this.cargarExercicios();
        this.$emit("cargarDatos");
        this.$emit("toggleExpand", idPlantilla);
      } catch (error) {
        console.error("❗Erro ao engadir exercicio á plantilla:", error);
      }
    },

    // rexistrar uso dunha plantilla
    async engadirPlantilla(plantilla) {
      const payload = {
        plantilla: plantilla.id_plantilla,
        usuario: this.idUsuario,
        data: this.dataHoxeISO,
      };
      try {
        const res = await fetch(
          "https://uplife-final.onrender.com/api/plantillas-uso/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify(payload),
          }
        );
        if (!res.ok) throw new Error("Erro ao rexistrar uso de plantilla");
        this.$emit("cargarPlantillasHoxe");
      } catch (error) {
        console.error("❗Erro ao rexistrar plantilla:", error);
      }
    },

    // obter nome da categoría segundo o id
    nomeCategoria(idCategoria) {
      const mapa = {
        1: "Perna",
        2: "Brazo",
        3: "Core",
        4: "Espalda",
        5: "Peito",
        6: "Todo corpo",
      };
      return mapa[idCategoria] || "Descoñecida";
    },
  },
};
</script>

<template>
  <div>
    <Cargando v-if="cargando"></Cargando>
    <div v-else id="divXeral">
      <h2>Historial de exercicios</h2>
      <p v-if="Object.keys(actividadesPorDia).length === 0" id="aviso">
        Non hai exercicios rexistrados
      </p>
      <div class="historial-scroll">
        <div
          v-for="(actividades, data) in actividadesPorDia"
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
            <li v-for="ex in actividades.exercicios" :key="ex.id_exercicio">
              <div class="fila-exercicio">
                <span>
                  [E] {{ ex.nome }} - {{ ex.repeticions }} - {{ ex.peso }}kg ({{
                    nomeCategoria(ex.categoria)
                  }})
                </span>
                <select v-model="plantillaSeleccionada[ex.id_exercicio]">
                  <option disabled value="">Seleccionar plantilla</option>
                  <option
                    v-for="p in plantillasUsuario"
                    :key="p.id_plantilla"
                    :value="p.id_plantilla"
                  >
                    {{ p.nome }}
                  </option>
                </select>
                <button
                  class="boton-dereita"
                  @click="
                    engadirExercicioAPlantilla(
                      ex,
                      plantillaSeleccionada[ex.id_exercicio]
                    )
                  "
                >
                  +
                </button>
              </div>
            </li>
          </ul>

          <span class="error">{{ erro }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}
.icona {
  height: 10%;
  width: 10%;
  background: white;
  border-radius: 4px;
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
}

.boton-dereita:hover {
  background-color: #6e4bd9;
}
</style>
