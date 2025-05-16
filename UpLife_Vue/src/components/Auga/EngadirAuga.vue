<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      cantidade: "",
      hora: "",
      erro: "",
    };
  },
  computed: {
    idUsuario() {
      const store = useUsuarioStore();
      return store.id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0]; // formato YYYY-MM-DD
    },
  },
  methods: {
    async engadirAuga() {
      this.erro = "";

      if (!this.cantidade || !this.hora) {
        this.erro = "Por favor, cobre todos os campos.";
        return;
      }

      const payload = {
        cantidade: this.cantidade,
        hora: this.hora,
        data: this.dataHoxeISO,
        usuario: this.idUsuario,
      };

      try {
        const usuarioStore = useUsuarioStore();
        await usuarioStore.cargarUsuario(this.idUsuario);
        await usuarioStore.actualizarDatos();
        const response = await fetch(
          "https://uplife-final.onrender.com/api/auga/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) {
          throw new Error("Erro ao engadir auga");
        }

        const resultado = await response.json();

        this.cantidade = "";
        this.hora = "";

        this.$emit("cargarAugaHoxe");
      } catch (error) {
        console.error("❗Erro no try-catch:", error);
        this.erro = "Houbo un erro ao engadir auga."; // Mensaje de error al usuario
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Engadir auga</h2>

      <label for="cantidade">Cantidade</label>
      <input
        type="number"
        min="0"
        id="cantidade"
        v-model="cantidade"
        placeholder="Cantidade(ml)"
      />

      <label for="hora">Hora</label>
      <input
        type="time"
        id="hora"
        v-model="hora"
        placeholder="Nome do exercicio"
      />

      <span v-if="erro" class="error">{{ erro }}</span>

      <button @click="engadirAuga">Engadir</button>
    </div>
  </div>
</template>

<style scoped>
.formulario button {
  margin-bottom: 4%;
  width: 100%;
}

label {
  color: white;
}
h2 {
  color: #7f5af0;
}
.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}
.engadir-container {
  display: flex;
  align-content: center;
  margin-top: 12%;
}
</style>
