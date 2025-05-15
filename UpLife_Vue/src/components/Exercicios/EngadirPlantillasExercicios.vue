<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      plantillas: [],
      error: "",
      plantillaSeleccionada: "",
    };
  },
  mounted() {
    this.cargarPlantillas();
  },
  computed: {
    idUsuario() {
      return useUsuarioStore().id;
    },
  },
  methods: {
    async cargarPlantillas() {
      const idUsuario = useUsuarioStore().id;

      try {
        const response = await fetch("http://localhost:8001/api/plantillas/");
        if (!response.ok) throw new Error("Erro ao cargar plantillas");

        const data = await response.json();

        // Mostrar solo plantillas del usuario actual
        this.plantillas = data.filter((p) => p.usuario === idUsuario);
        console.log("plantillas", data);

        console.log("plantillas cargadas", this.plantillas);
      } catch (error) {
        console.error("Erro cargando plantillas:", error);
      }
    },

    async engadirPlantilla() {
      this.error = "";
      if (!this.plantillaSeleccionada) {
        this.error = "Completa todos os campos";
        return;
      }

      const idUsuario = useUsuarioStore().id;
      const hoxe = new Date().toISOString().split("T")[0];

      try {
        const response = await fetch(
          "http://localhost:8001/api/plantillas-uso/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              usuario: idUsuario,
              plantilla: parseInt(this.plantillaSeleccionada),
              data: hoxe,
            }),
          }
        );

        if (!response.ok) throw new Error("Erro ao engadir uso da plantilla");

        this.$emit("cargarPlantillasHoxe");
        this.plantillaSeleccionada = "";
      } catch (error) {
        console.error("Erro engadindo uso de plantilla:", error);
        this.error = "Produciuse un erro ao engadir a plantilla.";
      }
    },
  },
};
</script>

<template>
  <div class="engadir-container">
    <form>
      <h2>Engadir plantilla</h2>

      <label for="select">Selecciona unha plantilla</label>
      <select id="select" v-model="plantillaSeleccionada">
        <option value="">Selecciona plantilla</option>
        <option
          v-for="plantilla in plantillas"
          :value="plantilla.id_plantilla"
          :key="plantilla.id_plantilla"
        >
          {{ plantilla.nome }}
        </option>
      </select>
      <span class="error">{{ error }}</span>

      <button @click.prevent="engadirPlantilla()">Engadir</button>
    </form>
  </div>
</template>

<style scoped>
button {
  margin-top: 3%;
  padding: 1%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 20%;
  height: 20%;
}
.engadir-container {
  height: 100%;
  width: 100%;
  overflow-y: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
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
@media (max-width: 768px) {
  .engadir-container {
    height: auto;
    width: 100%;
    overflow: hidden;
    padding: 1rem;
    box-sizing: border-box;
  }

  form {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  h2 {
    font-size: 1.3rem;
    text-align: center;
    margin-bottom: 1rem;
  }

  label {
    font-size: 1rem;
  }

  select {
    font-size: 1rem;
  }

  button {
    width: 100%;
    font-size: 1rem;
    padding: 0.75rem;
  }

  .error {
    font-size: 0.95rem;
    text-align: center;
  }
}
</style>
