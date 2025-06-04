<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  props: {
    dataSeleccionada: {
      type: Date,
      required: true,
    },
  },
  data() {
    return {
      tarefa: "",
      hora: "",
      erro: "",
    };
  },
  computed: {
    // obter id de usuario do store
    idUsuario() {
      const store = useUsuarioStore();
      return store.id;
    },

    // formatear data
    dataFormateada() {
      return this.dataSeleccionada
        .toLocaleDateString("gl-ES", {
          weekday: "long",
          year: "numeric",
          month: "long",
          day: "numeric",
        })
        .toUpperCase();
    },

    // obter hora mínima
    minHora() {
      const now = new Date();
      const hojeISO = now.toISOString().split("T")[0];
      const seleccionadaISO = this.dataSeleccionada.toISOString().split("T")[0];

      if (seleccionadaISO === hojeISO) {
        const horas = now.getHours().toString().padStart(2, "0");
        const minutos = now.getMinutes().toString().padStart(2, "0");
        return `${horas}:${minutos}`;
      }

      return "00:00";
    },
  },
  methods: {
    //engadir tarefa ao calendario
    async engadirTarefa() {
      this.erro = "";

      if (!this.tarefa) {
        this.erro = "Por favor, enche todos os campos.";
        return;
      }

      //comprobase que a hora non é unha hora pasada
      if (this.hora) {
        const [horaStr, minutoStr] = this.hora.split(":");
        const minutosIntroducidos =
          parseInt(horaStr, 10) * 60 + parseInt(minutoStr, 10);

        const ahora = new Date();
        const minutosAgora = ahora.getHours() * 60 + ahora.getMinutes();

        if (minutosIntroducidos < minutosAgora) {
          this.erro =
            "Non podes engadir unha tarefa para unha hora pasada de hoxe.";
          return;
        }
      }

      const payload = {
        hora: this.hora === "" ? null : this.hora,
        titulo: this.tarefa,
        data: this.dataSeleccionada.toLocaleDateString("en-CA"),
        completado: false,
        usuario: this.idUsuario,
      };

      const token = useUsuarioStore().token;
      if (!token) {
        this.erro = "Sesión expirada. Inicia sesión de novo.";
        return;
      }

      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/tarefas/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) throw new Error("Erro ao engadir tarefa");

        await response.json();

        this.tarefa = "";
        this.hora = "";
        this.$emit("cargarDatasConTarefas");
        this.$emit("comprobarRachas");
      } catch (error) {
        console.error("Erro:", error);
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Engadir tarefa</h2>
      <p class="data">
        <strong>{{ dataFormateada }}</strong>
      </p>
      <label for="hora">Hora</label>
      <input type="time" id="hora" v-model="hora" :min="minHora" />

      <label for="tarefa">Descrición da tarefa</label>
      <input
        type="text"
        id="tarefa"
        v-model="tarefa"
        placeholder="Escribe a túa tarefa"
      />

      <span v-if="erro" class="error">{{ erro }}</span>

      <button @click="engadirTarefa">Engadir</button>
    </div>
  </div>
</template>

<style scoped>
.formulario {
  padding-top: 0;
  width: 100%;
  margin-top: 11%;
}
.engadir-container {
  background-color: black;
  margin: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  text-align: left;
  display: flex;
  flex-direction: column;
  align-content: center;
  height: 100%;
  overflow-y: auto;
}

h2 {
  color: #7f5af0;
  font-size: x-large;
}

.data {
  color: white;
  font-weight: 500;
  font-size: 1rem;
  width: 100%;
  display: flex;
  justify-content: flex-start;
  margin: 0;
}

label {
  margin: 3% 0 1%;
  font-weight: 500;
  color: white;
}

input,
select {
  padding: 3%;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: medium;
  width: 100%;
  box-sizing: border-box;
}

button {
  padding: 3%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

button:hover {
  background-color: #3461cc;
}

.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}
@media (max-width: 768px) {
  .formulario {
    margin-top: 4vh;
    padding: 5vw;
  }

  h2 {
    font-size: 1.2rem;
  }

  .data {
    font-size: 0.95rem;
  }

  label {
    font-size: 0.9rem;
    margin-top: 5%;
  }

  input,
  select,
  button {
    font-size: 0.9rem;
    padding: 2.5% 3%;
  }

  .error {
    font-size: 0.85rem;
    margin-top: 1.5%;
  }
}
@media (min-width: 769px) and (max-width: 1370px) {
  .formulario {
    margin-top: 4vh;
    padding: 5vw;
  }

  h2 {
    font-size: 1.7rem;
  }

  .data {
    font-size: 0.95rem;
  }

  label {
    font-size: 1.1rem;
    margin-top: 5%;
  }

  input,
  select,
  button {
    font-size: 1.2rem;
    padding: 2.5% 3%;
  }

  .error {
    font-size: 0.85rem;
    margin-top: 1.5%;
  }
}
</style>
