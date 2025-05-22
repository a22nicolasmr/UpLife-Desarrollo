<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      exerciciosPorDia: {},
      actividadesPorDia: {},
      plantillasUsuario: [],
      plantillaSeleccionada: {},
    };
  },
  computed: {
    idUsuario() {
      return useUsuarioStore().id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
  },
  async mounted() {
    await this.cargarPlantillasUsuario();
    this.cargarExercicios();
  },
  methods: {
    async cargarPlantillasUsuario() {
      try {
        const res = await fetch(
          "https://uplife-final.onrender.com/api/plantillas/"
        );
        const data = await res.json();
        this.plantillasUsuario = data.filter(
          (p) => p.usuario === this.idUsuario
        );
      } catch (error) {
        console.error("Erro ao cargar plantillas:", error);
      }
    },

    async cargarExercicios() {
      try {
        const [resEx, resUsoPl] = await Promise.all([
          fetch("https://uplife-final.onrender.com/api/exercicios/"),
          fetch("https://uplife-final.onrender.com/api/plantillas-uso/"),
        ]);

        if (!resEx.ok || !resUsoPl.ok) throw new Error("Erro ao cargar datos");

        const exercicios = await resEx.json();
        const usosPlantilla = await resUsoPl.json();

        const seteDiasAtras = new Date();
        seteDiasAtras.setDate(seteDiasAtras.getDate() - 7);
        const seteDiasAtrasISO = seteDiasAtras.toISOString().split("T")[0];

        const userId = this.idUsuario;

        const exerciciosFiltrados = exercicios.filter(
          (e) => e.usuario === userId && e.data >= seteDiasAtrasISO
        );

        const usosFiltrados = await Promise.all(
          usosPlantilla
            .filter((u) => u.usuario === userId && u.data >= seteDiasAtrasISO)
            .map(async (uso) => {
              try {
                const plantillaResponse = await fetch(
                  `https://uplife-final.onrender.com/api/plantillas/${uso.plantilla}/`
                );
                const plantillaData = await plantillaResponse.json();
                return {
                  ...uso,
                  nome: plantillaData.nome,
                  id_plantilla: plantillaData.id_plantilla,
                  icona: plantillaData.icona,
                };
              } catch (error) {
                console.error(
                  `Erro cargando plantilla con id ${uso.plantilla}:`,
                  error
                );
                return null;
              }
            })
        );

        const usosFiltradosLimpios = usosFiltrados.filter(Boolean);

        const actividades = {};

        exerciciosFiltrados.forEach((ex) => {
          if (!actividades[ex.data])
            actividades[ex.data] = { exercicios: [], plantillas: [] };
          actividades[ex.data].exercicios.push(ex);
        });

        usosFiltradosLimpios.forEach((p) => {
          if (!actividades[p.data])
            actividades[p.data] = { exercicios: [], plantillas: [] };
          actividades[p.data].plantillas.push(p);
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
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          }
        );
        if (!res.ok) throw new Error("Erro ao engadir exercicio");
        this.$emit("cargarExerciciosHoxe");
      } catch (error) {
        console.error("❗Erro ao engadir exercicio:", error);
      }
    },

    async engadirExercicioAPlantilla(exercicio, idPlantilla) {
      try {
        // 1. Obtener la plantilla actual
        const plantillaRes = await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${idPlantilla}/`
        );
        if (!plantillaRes.ok)
          throw new Error("Non se puido cargar a plantilla");

        const plantilla = await plantillaRes.json();

        // 2. Obtener solo los IDs de los ejercicios existentes
        const idsExerciciosExistentes = plantilla.exercicios.map((e) =>
          typeof e === "object" ? e.id_exercicio : e
        );

        // 3. Añadir el nuevo ID si no está ya
        if (!idsExerciciosExistentes.includes(exercicio.id_exercicio)) {
          idsExerciciosExistentes.push(exercicio.id_exercicio);
        }

        // 4. Enviar PATCH con los IDs
        const patchRes = await fetch(
          `https://uplife-final.onrender.com/api/plantillas/${idPlantilla}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              exercicios: idsExerciciosExistentes,
            }),
          }
        );

        if (!patchRes.ok)
          throw new Error("Erro ao engadir exercicio á plantilla");

        console.log("✅ Exercicio engadido á plantilla con éxito");
        this.cargarExercicios();
        this.$emit("cargarDatos");
      } catch (error) {
        console.error("❗Erro ao engadir exercicio á plantilla:", error);
      }
    },
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
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          }
        );
        if (!res.ok) throw new Error("Erro ao rexistrar uso de plantilla");
        this.$emit("cargarPlantillasHoxe");
      } catch (error) {
        console.error("❗Erro ao rexistrar plantilla:", error);
      }
    },

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
  <div id="divXeral">
    <h2>Historial</h2>
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

        <ul>
          <li v-for="p in actividades.plantillas" :key="p.id_plantilla">
            <div class="fila-exercicio">
              <span id="spanPlantilla"> [P] {{ p.nome }} </span>
              <button class="boton-dereita" @click="engadirPlantilla(p)">
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
