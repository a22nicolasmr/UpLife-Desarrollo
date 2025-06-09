<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      nome: "",
      icona: "",
      erro: "",
      imaxes: [
        "/imaxes/musculo.png",
        "/imaxes/torso.png",
        "/imaxes/leg.png",
        "/imaxes/atras.png",
        "/imaxes/abdominales.png",
        "/imaxes/human-body.png",
      ],
      seleccionada: "",
    };
  },
  computed: {
    // obter usuario do storage
    idUsuario() {
      return useUsuarioStore().id;
    },

    // obter e formatear a data de hoxe
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },

    // obter token do usuario
    token() {
      return useUsuarioStore().token;
    },
  },
  methods: {
    // engadir unha plantilla nova
    async engadirNovaPlantilla() {
      this.erro = "";

      if (!this.nome || !this.icona) {
        this.erro = "Por favor, enche todos os campos.";
        return;
      }

      const payload = {
        nome: this.nome,
        icona: this.icona,
        usuario: this.idUsuario,
      };

      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/plantillas/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify(payload),
          }
        );

        const respostaTexto = await response.text();

        if (!response.ok) {
          throw new Error("Erro ao engadir plantillas");
        }

        this.nome = "";
        this.icona = "";

        // cargar datos en Plantillas
        this.$emit("cargarDatos");
      } catch (error) {
        this.erro = "Houbo un erro ao engadir plantillas.";
      }
    },
  },
  watch: {
    // seleccionar plantilla
    seleccionada(nova) {
      this.icona = nova;
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Nova plantilla</h2>

      <label for="nome">Nome</label>
      <input type="text" id="nome" v-model="nome" placeholder="Nome" />

      <p>Escolle unha icona para a plantilla</p>
      <div class="opcion-imaxes">
        <div
          v-for="(img, index) in imaxes"
          :key="index"
          class="imaxe"
          :class="{ seleccionada: img === seleccionada }"
          @click="seleccionada = img"
        >
          <img :src="img" alt="Opción de imaxe" tabindex="0" />
        </div>
      </div>

      <span v-if="erro" class="error">{{ erro }}</span>

      <button @click="engadirNovaPlantilla">Engadir</button>
    </div>
  </div>
</template>

<style scoped>
.engadir-container {
  height: 100%;
  width: 100%;
  overflow-y: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}
h2 {
  color: #7f5af0;
}

label,
p {
  color: white;
}

.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}

.formulario button {
  margin-bottom: 4%;
  width: 100%;
}

.opcion-imaxes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.imaxe {
  background-color: white;
  border-radius: 8px;
  cursor: pointer;
  border: 2px solid transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.imaxe img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.imaxe.seleccionada {
  border-color: #7f5af0;
}
</style>
