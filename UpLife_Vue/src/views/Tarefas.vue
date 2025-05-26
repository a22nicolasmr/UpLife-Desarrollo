<script>
import ListaTarefas from "@/components/Tarefas/ListaTarefas.vue";
import EngadirTarefas from "@/components/Tarefas/EngadirTarefas.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    ListaTarefas,
    EngadirTarefas,
  },
  data() {
    return {
      rTarefas: 0,
      rExercicios: 0,
      rComidas: 0,
      rAuga: 0,
      dataPasada: false,
      componenteActivo: "lista",
      dataSeleccionada: new Date(),
      attrs: [],
      token: "",
      valorMedallas: [
        {
          id_medalla: 4,
          completado: true,
        },
      ],
      advertencias: {
        tarefas: false,
        exercicios: false,
        comidas: false,
        auga: false,
      },
    };
  },

  // cando se carga a vista, cargar as datas con tarefas, comprobar rachas e medallas do usuario
  async mounted() {
    this.token = localStorage.getItem("token");
    if (!this.token) {
      console.warn("🔴 Token no encontrado, redirigiendo al login...");
      this.$router.push({ name: "login" });
      return;
    }
    await this.cargarDatasConTarefas();
    await this.comprobarRachas();
    await this.comprobarMedallas();
  },

  methods: {
    // comprobar se os requerimentos das medallas se cumplen
    async comprobarMedallas() {
      await this.comprobarRachas();
      const valorMedallas = [];
      let seCompletoAlguna = false;

      const agregarMedalla = (id, completado) => {
        if (completado) seCompletoAlguna = true;
        valorMedallas.push({ id_medalla: id, completado });
      };

      // Medallas base
      agregarMedalla(4, true);
      agregarMedalla(5, this.rComidas >= 7);
      agregarMedalla(6, this.rExercicios >= 5);
      agregarMedalla(7, this.rAuga >= 7);
      agregarMedalla(8, this.rTarefas >= 5);
      agregarMedalla(
        9,
        this.rComidas >= 7 && this.rExercicios >= 7 && this.rAuga >= 7
      );
      agregarMedalla(10, false); // Lógica pendiente

      // Medalla 11 (plantillas)
      try {
        const [plantillasRes, usosRes] = await Promise.all([
          fetch("https://uplife-final.onrender.com/api/plantillas/", {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }),
          fetch("https://uplife-final.onrender.com/api/plantillas-uso/", {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }),
        ]);

        const [plantillas, usos] = await Promise.all([
          plantillasRes.json(),
          usosRes.json(),
        ]);

        const idUsuario = useUsuarioStore().id;

        const plantillasUsuario = plantillas.filter(
          (p) => p.usuario === idUsuario
        );

        const usosPorPlantilla = {};
        usos.forEach((u) => {
          if (u.usuario !== idUsuario) return;
          const id = u.plantilla?.id_plantilla;
          if (!id) return;
          if (!usosPorPlantilla[id]) usosPorPlantilla[id] = new Set();
          usosPorPlantilla[id].add(u.data);
        });

        const usadasSuficiente = plantillasUsuario.filter((p) => {
          const usosSet = usosPorPlantilla[p.id_plantilla];
          return usosSet && usosSet.size >= 2;
        });

        agregarMedalla(11, usadasSuficiente.length >= 3);
      } catch (error) {
        console.error("❌ Erro ao comprobar medalla de plantillas:", error);
        agregarMedalla(11, false);
      }

      agregarMedalla(
        12,
        this.rComidas >= 90 &&
          this.rExercicios >= 90 &&
          this.rAuga >= 90 &&
          this.rTarefas >= 90
      );

      agregarMedalla(
        13,
        this.rComidas >= 365 &&
          this.rExercicios >= 365 &&
          this.rAuga >= 365 &&
          this.rTarefas >= 365
      );

      this.valorMedallas = valorMedallas;
      this.$emit("mandarRachas", this.valorMedallas);

      const usuarioStore = useUsuarioStore();
      const medallasPrevias = Array.isArray(usuarioStore.medallas)
        ? usuarioStore.medallas
        : Object.values(usuarioStore.medallas || []);

      const medallasMostradas =
        JSON.parse(localStorage.getItem("medallasMostradas")) || [];

      let nuevasParaMostrar = [];

      for (const nueva of valorMedallas) {
        const previa = medallasPrevias.find(
          (m) => m.id_medalla === nueva.id_medalla
        );
        const yaEstabaCompletada = previa?.completado;
        const yaMostrada = medallasMostradas.includes(nueva.id_medalla);

        if (!yaEstabaCompletada && nueva.completado && !yaMostrada) {
          nuevasParaMostrar.push(nueva.id_medalla);
        }
      }

      if (nuevasParaMostrar.length > 0) {
        this.$emit("abrirVentaMedallas");

        const actualizado = [
          ...new Set([...medallasMostradas, ...nuevasParaMostrar]),
        ];
        localStorage.setItem("medallasMostradas", JSON.stringify(actualizado));
      }

      usuarioStore.updateNumeroMedallas();
      usuarioStore.cargarMedallas();

      return valorMedallas;
    },
    // comprobar as rachas do usuario en función das datas anteriores a data actual
    // en Tarefas tamén comproba se están completadas
    async comprobarRachas() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      const urls = [
        {
          key: "auga",
          var: "rAuga",
          url: "https://uplife-final.onrender.com/api/auga/",
        },
        {
          key: "comidas",
          var: "rComidas",
          url: "https://uplife-final.onrender.com/api/comidas/",
        },
        {
          key: "tarefas",
          var: "rTarefas",
          url: "https://uplife-final.onrender.com/api/tarefas/",
        },
      ];

      // reiniciar rachas
      this.rAuga = 0;
      this.rComidas = 0;
      this.rExercicios = 0;
      this.rTarefas = 0;

      // procesar augas, comidas, tarefas
      for (const item of urls) {
        const res = await fetch(item.url, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });
        const data = await res.json();

        const userData = data.filter((entry) => {
          const esUsuario = entry.usuario === idUsuario;
          const tieneFechaValida =
            entry.data &&
            entry.data.trim() !== "" &&
            entry.data <= new Date().toISOString().split("T")[0];
          const estaCompletado =
            item.key !== "tarefas" || entry.completado === true;

          return esUsuario && tieneFechaValida && estaCompletado;
        });

        const fechas = [...new Set(userData.map((entry) => entry.data))]
          .sort()
          .reverse();

        let racha = 0;
        let hoy = new Date().toISOString().split("T")[0];

        const hayHoy = userData.some(
          (entry) => entry.data === new Date().toISOString().split("T")[0]
        );
        this.advertencias[item.key] = !hayHoy;

        for (const fecha of fechas) {
          if (fecha === hoy) {
            racha++;
            hoy = new Date(new Date(hoy).getTime() - 86400000)
              .toISOString()
              .split("T")[0];
          } else {
            break;
          }
        }

        this[item.var] = racha;
      }

      // calcular rExercicios usando exercicios + plantillas de exercicios
      try {
        const [resEx, resUso] = await Promise.all([
          fetch("https://uplife-final.onrender.com/api/exercicios/", {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }),
          fetch("https://uplife-final.onrender.com/api/plantillas-uso/", {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }),
        ]);

        const [exercicios, usos] = await Promise.all([
          resEx.json(),
          resUso.json(),
        ]);

        const exerciciosValidos = exercicios
          .filter(
            (e) =>
              e.usuario === idUsuario &&
              e.data &&
              e.data <= new Date().toISOString().split("T")[0]
          )
          .map((e) => e.data);

        const usosValidos = usos
          .filter(
            (u) =>
              u.usuario === idUsuario &&
              u.data &&
              u.data <= new Date().toISOString().split("T")[0]
          )
          .map((u) => u.data);

        const todasFechas = new Set([...exerciciosValidos, ...usosValidos]);
        const fechasUnicasOrdenadas = [...todasFechas].sort().reverse();

        // calcular racha consecutiva
        let rachaEx = 0;
        let hoy = new Date().toISOString().split("T")[0];

        const hayHoy = [...exerciciosValidos, ...usosValidos].includes(hoy);
        this.advertencias.exercicios = !hayHoy;

        for (const fecha of fechasUnicasOrdenadas) {
          if (fecha === hoy) {
            rachaEx++;
            hoy = new Date(new Date(hoy).getTime() - 86400000)
              .toISOString()
              .split("T")[0];
          } else {
            break;
          }
        }

        this.rExercicios = rachaEx;
      } catch (error) {
        console.error(
          "Erro ao comprobar exercicios e usos de plantillas:",
          error
        );
      }
    },
    // comprobar se hai tarefas para unha data
    async comprobarTarefasNaData(date) {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/tarefas/`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const tarefas = await response.json();

        const tarefasNaData = tarefas.filter(
          (t) =>
            t.usuario === idUsuario &&
            new Date(t.data).toDateString() === date.toDateString()
        );

        const todasCompletadas =
          tarefasNaData.length > 0 &&
          tarefasNaData.every((t) => t.completado === true);

        if (tarefasNaData.length === 0 || todasCompletadas) {
          this.componenteActivo = "engadir";
        } else {
          this.componenteActivo = "lista";
        }
      } catch (error) {
        console.error("Erro ao comprobar tarefas na data", error);
      }
    },
    // enviar as tarefas que teñen hora a App para executar VentáAviso de App
    reenviarTarefasConHora(tarefas) {
      this.$emit("emitirDatasConTarefas", tarefas);
    },

    // obter fechas deshabilitadas
    getFechasDeshabilitadas({ date }) {
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0);

      const comparar = new Date(date);
      comparar.setHours(0, 0, 0, 0);

      return comparar < hoy;
    },

    // seleccionar data no calendario
    seleccionarData(dia) {
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0); //eliminar horas para comparar só a data

      if (dia.date < hoy) return;

      this.dataSeleccionada = dia.date;
      this.comprobarTarefasNaData(this.dataSeleccionada);

      // scrollear ata as tarefas da data seleccionada
      this.$nextTick(() => {
        if (this.$refs.listaTarefasRef?.scrollAtaData) {
          this.$refs.listaTarefasRef.scrollAtaData(dia.date);
        }
      });
    },

    // os días que teñan tarefas serán marcados cunha cor azul claro usando attrs de vc-calendar
    actualizarDatasConTarefas(datas) {
      const today = new Date();
      const todayISO = today.toISOString().split("T")[0];

      const todayAttr = {
        key: "today",
        highlight: {
          color: "#003366",
          fillMode: "solid",
        },
        dates: today,
        order: 100,
        customData: { esHoy: true },
      };

      const taskAttrs = datas
        .filter((date) => date !== todayISO)
        .map((date) => ({
          key: `task-${date}`,
          highlight: {
            color: "#add8e6",
            fillMode: "light",
          },
          dates: new Date(date),
          order: 1,
        }));

      this.attrs = [todayAttr, ...taskAttrs];
    },
    // obter as tarefas filtradas por usuario e data
    async cargarDatasConTarefas() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/tarefas/`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const tarefas = await response.json();

        const datasUnicas = [
          ...new Set(
            tarefas.filter((t) => t.usuario === idUsuario).map((t) => t.data)
          ),
        ];

        this.actualizarDatasConTarefas(datasUnicas);
        this.componenteActivo = "lista";
      } catch (error) {
        console.error("Erro ao cargar datas con tarefas", error);
      }
    },
  },
  computed: {
    // deshabilitar todas aquelas datas por debaixo da data de hoxe
    disabledDates() {
      return [
        {
          end: new Date(new Date().setDate(new Date().getDate() - 1)),
        },
      ];
    },
  },
};
</script>

<template>
  <div id="divXeral">
    <h1 class="titulo">Tarefas</h1>
    <div class="divsArriba">
      <div id="izquierda">
        <div>
          <p>Racha de tarefas</p>
          <p>{{ rTarefas }}</p>
          <p v-if="advertencias.tarefas" class="advertencia">
            ✔ Fai unha tarefa!
          </p>
        </div>
        <div>
          <img src="/imaxes/task.png" alt="Icona tarefas" />
        </div>
      </div>

      <div id="exercicio">
        <div>
          <p>Racha de exercicios</p>
          <p>{{ rExercicios }}</p>
          <p v-if="advertencias.exercicios" class="advertencia">
            💪 Fai un exercicio hoxe!
          </p>
        </div>
        <div>
          <img src="/imaxes/exercise.png" alt="Icona exercicios" />
        </div>
      </div>

      <div id="comidas">
        <div>
          <p>Racha de comidas</p>
          <p>{{ rComidas }}</p>
          <p v-if="advertencias.comidas" class="advertencia">
            🍽️ Rexistra a túa comida!
          </p>
        </div>
        <div>
          <img src="/imaxes/diet.png" alt="Icona comidas" />
        </div>
      </div>

      <div id="auga">
        <div>
          <p>Racha de auga</p>
          <p class="centro">{{ rAuga }}</p>
          <p v-if="advertencias.auga" class="advertencia">
            💧 Rexistra a túa auga!
          </p>
        </div>
        <div>
          <img src="/imaxes/water-bottle.png" alt="Icona auga" />
        </div>
      </div>
    </div>

    <div class="tarxetas">
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'lista' }"
        @click="componenteActivo = 'lista'"
      >
        Lista
      </div>
      <div
        class="tarxeta"
        :class="{ inactiva: componenteActivo !== 'engadir' }"
        @click="componenteActivo = 'engadir'"
      >
        Engadir
      </div>
    </div>

    <div class="tarefas-layout">
      <div class="calendario">
        <vc-calendar
          :key="attrs.length"
          :attributes="attrs"
          @dayclick="seleccionarData"
          :min-date="new Date()"
          :disabled-dates="disabledDates"
        />
      </div>

      <div class="lateral">
        <ListaTarefas
          v-if="componenteActivo === 'lista'"
          ref="listaTarefasRef"
          :dataSeleccionada="dataSeleccionada"
          @datas-con-tarefas="reenviarTarefasConHora"
          @cargarDatasConTarefas="cargarDatasConTarefas"
          @comprobarRachas="comprobarRachas"
        />

        <EngadirTarefas
          v-if="componenteActivo === 'engadir'"
          :dataSeleccionada="dataSeleccionada"
          @cargarDatasConTarefas="cargarDatasConTarefas"
          @comprobarRachas="comprobarRachas"
        />
      </div>
    </div>
  </div>
</template>

<style>
#izquierda,
#exercicio,
#auga,
#comidas {
  display: flex;
  padding: 1%;
  padding-right: 2%;
}
#izquierda p:nth-of-type(2),
#exercicio p:nth-of-type(2),
#auga p:nth-of-type(2),
#comidas p:nth-of-type(2) {
  font-size: x-large;
}
#divXeral {
  display: flex;
  flex-direction: column;
  min-height: 100%; /* Esto cubre la ventana completa */
  box-sizing: border-box; /* <-- Muy útil si usas paddings/margins */
}

.divsArriba img {
  height: 8vh;
  width: 8vh;
  padding-top: 60%;
}
.divsArriba {
  display: flex;
  flex: 0.5;
  justify-content: space-between;
  margin-right: 4%;
  margin-bottom: 2%;
}
.divsArriba > div {
  background-color: white;
  border-radius: 8px;
}
.tarefas-wrapper {
  background-color: #f5f6f8;
}

.titulo {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
  margin-bottom: 2%;
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
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.tarefas-layout {
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-right: 4%;
  height: 100%;
  margin-bottom: 2%;
}

/* Calendario */
.calendario {
  display: flex;
  flex: 1;
  background-color: white;
  box-sizing: border-box;
}
h1 {
  display: flex;
  align-self: flex-start;
  margin-bottom: 0;
  color: #7f5af0;
}
/* Compoñente lateral */
.lateral {
  width: 40%;
  background-color: #1c1c1c;
  color: white;
  box-sizing: border-box;
}

/* v-calendar estilos */
.vc-container {
  width: 100% !important;
  font-size: medium !important;
  padding: 2%;
  border: none !important;
  height: 100%;
}
.vc-weeks {
  margin-top: 5%;
}
.vc-week {
  padding-top: 3.5%;
}
.vc-weekdays {
  padding-top: 1%;
}
.vc-day-content {
  font-size: large !important;
  margin: 5 auto !important;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;

  transition: background-color 0.3s, transform 0.2s;
}
@media (max-width: 768px) {
  .tarefas-layout {
    flex-direction: column;
    height: auto;
    margin-right: 0;
  }

  .calendario,
  .lateral {
    width: 100%;
    height: auto;
  }

  .divsArriba {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1rem;
  }

  .divsArriba > div {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: white;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .divsArriba img {
    height: 5.5vh;
    width: 5.5vh;
    margin-top: 0.5rem;
  }

  .divsArriba p {
    margin: 0.2rem 0;
    text-align: center;
    font-size: 0.9rem;
  }
  #exercicio div:nth-of-type(1),
  #auga div:nth-of-type(1),
  #comidas div:nth-of-type(1) {
    margin-top: 4%;
  }
  #izquierda p:nth-of-type(2),
  #exercicio p:nth-of-type(2),
  #auga p:nth-of-type(2),
  #comidas p:nth-of-type(2) {
    font-size: 1.1rem;
    font-weight: bold;
    color: #4880ff;
  }

  .advertencia {
    font-size: 0.75rem;
    color: #ff4d4d;
    margin-top: 0.3rem;
  }

  .tarxetas {
    justify-content: center;
  }

  .tarxeta {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    border-radius: 0.5rem 0.5rem 0 0;
  }

  .tarxeta.inactiva {
    background-color: #ccc;
    color: #fff;
  }

  html,
  body {
    overflow-x: hidden;
  }
}
</style>
