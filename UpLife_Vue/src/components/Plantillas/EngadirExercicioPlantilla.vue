<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      plantillas: [],
      plantillaSeleccionada: "",
      nomeExercicio: "",
      categorias: [],
      categoriaSeleccionada: 0,
      repeticions: "",
      peso: null,
      erro: "",
    };
  },
  props: {
    plantillaSeleccionadaMandar: "",
  },
  mounted() {
    this.cargarDatos();
  },
  watch: {
    plantillaSeleccionadaMandar: {
      immediate: true,
      handler(novoValor) {
        if (novoValor != null) {
          this.plantillaSeleccionada = Number(novoValor);

          console.log("🔄 novoValor asignado:", novoValor);
        } else {
          console.log("⚠ novoValor é null ou undefined");
        }
      },
    },
  },
  methods: {
    async engadirExercicio() {
      console.log("engadir exercicios");

      this.comprobarCampos();
      if (this.erro) return;

      try {
        const usuarioStore = useUsuarioStore();
        const idUsuario = usuarioStore.id;

        const exercicioPayload = {
          nome: this.nomeExercicio,
          repeticions: this.repeticions,
          peso: parseFloat(this.peso),
          usuario: idUsuario,
          categoria: parseInt(this.categoriaSeleccionada),
        };

        const resEx = await fetch("http://localhost:8001/api/exercicios/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(exercicioPayload),
        });

        if (!resEx.ok) throw new Error("Erro ao crear exercicio");
        const exercicioCreado = await resEx.json();
        console.log("exercicio creado ", exercicioCreado);

        await this.cargarDatos();
        const plantilla = this.plantillas.find(
          (p) => p.id_plantilla === this.plantillaSeleccionada
        );

        const novaLista = [
          ...(plantilla.exercicios || []).map((ex) => Number(ex.id_exercicio)),
          Number(exercicioCreado.id_exercicio),
        ];

        console.log("✅ Nova lista a enviar:", novaLista);

        const resPatch = await fetch(
          `http://localhost:8001/api/plantillas/${this.plantillaSeleccionada}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ exercicios: novaLista }),
          }
        );

        if (!resPatch.ok)
          throw new Error("Erro ao engadir exercicio á plantilla");

        const responsePatchData = await resPatch.json();
        console.log("📦 Resposta do PATCH:", responsePatchData);

        // recargar datos para actualizar a lista de plantillas
        await this.cargarDatos();

        // resetear os campos
        this.nomeExercicio = "";
        this.repeticions = "";
        this.peso = null;
        this.categoriaSeleccionada = "";
        this.erro = "";
        // window.location.reload();
        this.$emit("cargarDatos");
      } catch (error) {
        console.error("❌ Erro engadindo exercicio:", error);
        this.erro = "Houbo un erro ao engadir o exercicio.";
      }
    },

    async cargarDatos() {
      console.log("cargar datos ejecutado");

      try {
        const usuarioStore = useUsuarioStore();
        const idUsuario = usuarioStore.id;
        const response = await fetch(`http://localhost:8001/api/plantillas/`);

        if (!response.ok) throw new Error("Erro ao cargar plantillas");
        const plantillas = await response.json();

        this.plantillas = plantillas.filter((p) => p.usuario === idUsuario);

        const response2 = await fetch(`http://localhost:8001/api/categorias/`);
        if (!response2.ok) throw new Error("Erro ao cargar categorias");
        const categorias = await response2.json();
        this.categorias = categorias;
      } catch (error) {
        console.error("Erro cargando datos:", error);
      }
    },
    comprobarCampos() {
      console.log(
        this.plantillaSeleccionada,
        this.nomeExercicio,
        this.categoriaSeleccionada,
        this.repeticions,
        this.peso
      );

      this.erro = "";
      if (
        !this.plantillaSeleccionada ||
        !this.nomeExercicio.trim() ||
        !this.categoriaSeleccionada ||
        !this.repeticions.trim() ||
        this.peso === null ||
        this.peso <= 0
      ) {
        this.erro = "Por favor, cobre todos os campos.";
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <div class="formulario">
      <h2>Engadir exercicio a plantilla</h2>

      <label for="selectPlantilla">Plantilla</label>
      <select id="selectPlantilla" v-model.number="plantillaSeleccionada">
        <option value="">Selecciona unha opción</option>
        <option
          v-for="plantilla in plantillas"
          :key="plantilla.id_plantilla"
          :value="plantilla.id_plantilla"
        >
          {{ plantilla.nome }}
        </option>
      </select>

      <label for="nomeExercicio">Nome exercicio</label>
      <input
        id="nomeExercicio"
        type="text"
        v-model="nomeExercicio"
        placeholder="Nome do exercicio"
      />

      <label for="selectCategoria">Categoría</label>
      <select id="selectCategoria" v-model.number="categoriaSeleccionada">
        <option value="">Selecciona unha categoría</option>
        <option
          v-for="categoria in categorias"
          :key="categoria.id_categoria"
          :value="categoria.id_categoria"
        >
          {{ categoria.nome }}
        </option>
      </select>

      <label for="repeticions">Repeticións</label>
      <input
        id="repeticions"
        type="text"
        v-model="repeticions"
        placeholder="Exemplo: 3x10"
      />

      <label for="peso">Peso (kg)</label>
      <input type="number" id="peso" v-model.number="peso" min="0" step="0.1" />

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
  margin-top: 10%;
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
