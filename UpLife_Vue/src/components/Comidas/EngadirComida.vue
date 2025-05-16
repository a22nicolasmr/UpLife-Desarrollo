<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  props: {
    grupoSeleccionadoMandar: "",
  },
  data() {
    return {
      grupos: [],
      grupoSeleccionado: "",
      nomeComida: "",
      peso: null,
      graxas: null,
      carbohidratos: null,
      proteinas: null,
      calorias: null,
      erro: "",
    };
  },
  watch: {
    grupoSeleccionadoMandar: {
      immediate: true,
      handler(novoValor) {
        if (novoValor != null) {
          this.grupoSeleccionado = Number(novoValor);

          console.log("🔄 novoValor asignado:", novoValor);
        } else {
          console.log("⚠ novoValor é null ou undefined");
        }
      },
    },
  },
  mounted() {
    this.cargarDatos();
  },
  methods: {
    dataHoxeISO() {
      return new Date().toISOString().split("T")[0];
    },
    async cargarDatos() {
      try {
        const usuarioStore = useUsuarioStore();
        const idUsuario = usuarioStore.id;
        const response = await fetch(
          `https://uplife-final.onrender.com/api/grupos/`
        );
        if (!response.ok) throw new Error("Erro ao cargar grupos");
        const grupos = await response.json();
        this.grupos = grupos.filter((p) => p.usuario === idUsuario);
      } catch (error) {
        console.error("Erro cargando datos:", error);
      }
    },
    comprobarCampos() {
      this.erro = "";
      console.log(
        "grupo",
        this.grupoSeleccionado,
        "nome",
        this.nomeComida,
        "peso",
        this.peso,
        "graxas",
        this.graxas,
        "carbohi",
        this.carbohidratos,
        "proteinas",
        this.proteinas,
        "calorias",
        this.calorias
      );

      if (
        !this.grupoSeleccionado ||
        !this.nomeComida.trim() ||
        this.peso === null ||
        this.peso <= 0 ||
        this.graxas === null ||
        this.carbohidratos === null ||
        this.proteinas === null ||
        this.calorias === null
      ) {
        this.erro = "Por favor, cobre todos os campos.";
      }
    },
    async engadirComida() {
      this.comprobarCampos();
      if (this.erro) return;

      try {
        const usuarioStore = useUsuarioStore();
        const idUsuario = usuarioStore.id;

        // 1. Crear comida
        const comidaPayload = {
          nome: this.nomeComida,
          peso: this.peso,
          graxas: this.graxas,
          carbohidratos: this.carbohidratos,
          proteinas: this.proteinas,
          calorias: this.calorias,
          data: this.dataHoxeISO(),
          usuario: idUsuario,
        };

        const resComida = await fetch(
          "https://uplife-final.onrender.com/api/comidas/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(comidaPayload),
          }
        );

        if (!resComida.ok) throw new Error("Erro ao crear comida");
        const comidaCreada = await resComida.json();

        // 2. Engadir comida ao grupo
        const grupo = this.grupos.find(
          (g) => Number(g.id_grupo) === Number(this.grupoSeleccionado)
        );

        const novaLista = [
          ...(grupo.comidas || []).map((c) => Number(c.id_comida)),
          Number(comidaCreada.id_comida),
        ];

        const resPatch = await fetch(
          `https://uplife-final.onrender.com/api/grupos/${this.grupoSeleccionado}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ comidas: novaLista }),
          }
        );

        if (!resPatch.ok) throw new Error("Erro ao engadir comida ao grupo");

        // Resetear campos
        this.nomeComida = "";
        this.peso = null;
        this.graxas = null;
        this.carbohidratos = null;
        this.proteinas = null;
        this.calorias = null;
        this.grupoSeleccionado = "";
        this.erro = "";

        this.$emit("cargarDatos");
      } catch (error) {
        console.error("❌ Erro engadindo comida:", error);
        this.erro = "Houbo un erro ao engadir a comida.";
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Engadir comida a grupo</h2>

      <label for="selectgrupo">Grupo</label>
      <select id="selectgrupo" v-model="grupoSeleccionado">
        <option value="">Selecciona unha opción</option>
        <option
          v-for="grupo in grupos"
          :key="grupo.id_grupo"
          :value="grupo.id_grupo"
        >
          {{ grupo.nome }}
        </option>
      </select>

      <label for="nomeComida">Nome comida</label>
      <input
        id="nomeComida"
        type="text"
        v-model="nomeComida"
        placeholder="Nome da comida"
      />

      <label for="peso">Peso (g)</label>
      <input type="number" id="peso" v-model.number="peso" min="0" step="0.1" />
      <p>Cantidadades por 100g</p>

      <div class="grid-numeros">
        <div>
          <input
            type="number"
            id="graxas"
            v-model.number="graxas"
            min="0"
            step="0.1"
            placeholder="Graxas"
          />
        </div>

        <div>
          <input
            type="number"
            id="carbohidratos"
            v-model.number="carbohidratos"
            min="0"
            step="0.1"
            placeholder="Carbohidratos"
          />
        </div>

        <div>
          <input
            type="number"
            id="proteinas"
            v-model.number="proteinas"
            min="0"
            step="0.1"
            placeholder="Proteínas"
          />
        </div>

        <div>
          <input
            type="number"
            id="calorias"
            v-model.number="calorias"
            min="0"
            step="0.1"
            placeholder="Calorías"
          />
        </div>
      </div>

      <span v-if="erro" class="error">{{ erro }}</span>

      <button @click.prevent="engadirComida">Engadir</button>
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

.grid-numeros {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3%;
  width: 100%;
}

.grid-numeros div {
  display: flex;
  flex-direction: column;
  margin-bottom: 18%;
}

.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}
</style>
