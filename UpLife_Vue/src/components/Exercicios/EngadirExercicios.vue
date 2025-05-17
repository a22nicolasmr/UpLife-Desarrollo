<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      nome: "",
      repeticions: "",
      peso: null,
      categoriaSeleccionada: "",
      categorias: ["Peito", "Espalda", "Core", "Brazo", "Perna", "Todo corpo"],
      erro: "",
    };
  },
  computed: {
    //obter usuario do storage e data de hoxe
    idUsuario() {
      const store = useUsuarioStore();
      return store.id;
    },
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
  },
  methods: {
    //validar formulario
    comprobarCampos() {
      this.erro = "";
      console.log(
        "nome",
        this.nome,
        "categoria",
        this.categoriaSeleccionada,
        "repeticions",
        this.repeticions,
        "peso",
        this.peso
      );

      if (
        !this.nome ||
        !this.categoriaSeleccionada ||
        !this.repeticions ||
        !this.peso
      ) {
        this.erro = "Por favor, cobre todos os campos.";
        return false;
      }

      return true;
    },

    //filtrar categoría por id
    obterIdCategoriaPorId(id) {
      const categoria = this.categorias.find((c) => c.id === parseInt(id));
      return categoria ? categoria.id : null;
    },

    //obter nome da categoría por id
    obterIdCategoria(nome) {
      const mapa = {
        Perna: 1,
        Brazo: 2,
        Core: 3,
        Espalda: 4,
        Peito: 5,
        "Todo corpo": 6,
      };
      return mapa[nome];
    },

    //engadir un novo exercicio
    async engadirExercicio() {
      if (!this.comprobarCampos()) return;

      if (this.erro) return;

      try {
        const usuarioStore = useUsuarioStore();
        const idUsuario = usuarioStore.id;

        const idCategoria = this.obterIdCategoria(this.categoriaSeleccionada);

        const exercicioPayload = {
          categoria: idCategoria,
          nome: this.nome,
          repeticions: this.repeticions,
          peso: parseFloat(this.peso),
          data: new Date().toISOString().split("T")[0],
          usuario: idUsuario,
        };

        const resEx = await fetch(
          "https://uplife-final.onrender.com/api/exercicios/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(exercicioPayload),
          }
        );

        if (!resEx.ok) throw new Error("Erro ao crear exercicio");

        //limpar campos
        this.nome = "";
        this.repeticions = "";
        this.peso = 0;
        this.categoriaSeleccionada = "";
        this.erro = "";
        this.$emit("cargarExerciciosHoxe");
      } catch (error) {
        console.error("❌ Erro engadindo exercicio:", error);
        this.erro = "Houbo un erro ao engadir o exercicio.";
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Engadir exercicio</h2>

      <label for="categoria">Categoría</label>
      <select v-model="categoriaSeleccionada" id="categoria">
        <option disabled value="">Selecciona unha categoría</option>
        <option v-for="cat in categorias" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>

      <label for="nome">Nome do exercicio</label>
      <input
        type="text"
        id="nome"
        v-model="nome"
        placeholder="Nome do exercicio"
      />
      <label for="repeticions">Repeticións</label>
      <input
        type="text"
        id="repeticions"
        v-model="repeticions"
        placeholder="Exemplo: 3x10"
      />

      <label for="peso">Peso (kg)</label>
      <input type="number" id="peso" v-model="peso" min="0" step="0.1" />

      <span v-if="erro" class="error">{{ erro }}</span>

      <button @click.prevent="engadirExercicio">Engadir</button>
    </div>
  </div>
</template>

<style scoped>
.formulario button {
  margin-bottom: 4%;
  width: 100%;
}
.formulario label {
  width: 100%;
}
.formulario {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 2%;
}
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
p,
label {
  color: white;
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
.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}
</style>
