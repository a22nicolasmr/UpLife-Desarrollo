<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      nome: "",
      icona: "",
      erro: "",
      imaxes: [
        "/imaxes/morning.png",
        "/imaxes/sunset.png",
        "/imaxes/sun.png",
        "/imaxes/lunch.png",
        "/imaxes/fruta.png",
        "/imaxes/pizza.png",
      ],
      seleccionada: "",
    };
  },
  computed: {
    idUsuario() {
      const store = useUsuarioStore();
      return store.id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
  },
  methods: {
    async engadirNovoGrupo() {
      this.erro = "";

      if (!this.nome || !this.icona) {
        this.erro = "Por favor, cobre todos os campos.";
        return;
      }

      const payload = {
        nome: this.nome,
        icona: this.icona,
        usuario: this.idUsuario,
      };

      try {
        const response = await fetch("http://localhost:8001/api/grupos/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const respostaTexto = await response.text();
        console.log(respostaTexto);

        if (!response.ok) {
          throw new Error("Erro ao engadir plantillas");
        }

        this.nome = "";
        this.icona = "";
        this.$emit("cargarDatos");
      } catch (error) {
        this.erro = "Houbo un erro ao engadir plantillas.";
      }
    },
  },
  watch: {
    seleccionada(nova) {
      this.icona = nova;
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Novo grupo</h2>

      <label for="nome">Nome</label>
      <input type="text" id="nome" v-model="nome" placeholder="Nome" />

      <p>Escolle unha icona para o grupo</p>
      <div class="opcion-imaxes">
        <div
          v-for="(img, index) in imaxes"
          :key="index"
          class="imaxe"
          :class="{ seleccionada: img === seleccionada }"
          @click="seleccionada = img"
        >
          <img :src="img" alt="Opción de imaxe" />
        </div>
      </div>

      <span v-if="erro" class="error">{{ erro }}</span>

      <button @click="engadirNovoGrupo">Engadir</button>
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
