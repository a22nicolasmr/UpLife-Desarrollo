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
  methods: {
    comprobarError() {
      if (!this.plantillaSeleccionada) {
        this.error = "Completa todos os campos";
        return false;
      }
      return true;
    },
    async cargarPlantillas() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;

      try {
        const response = await fetch("http://localhost:8001/api/plantillas/");
        if (!response.ok) throw new Error("Erro ao cargar plantillas");

        const plantillas = await response.json();
        const plantillasFiltradas = plantillas
          .filter((p) => p.usuario === idUsuario)
          .map((p2) => ({
            id_plantilla: p2.id_plantilla,
            nome: p2.nome,
          }));
        this.plantillas = plantillasFiltradas;
      } catch (error) {
        console.error("Erro cargando exercicios:", error);
      }
    },
    async engadirPlantilla() {
      this.error = "";
      if (!this.comprobarError()) return;

      try {
        const plantilla = this.plantillas.find(
          (p) => p.nome === this.plantillaSeleccionada
        );

        if (!plantilla) {
          this.error = "Plantilla non atopada.";
          return;
        }

        // Obter plantilla completa para acceder ao campo datas
        const res = await fetch(
          `http://localhost:8001/api/plantillas/${plantilla.id_plantilla}/`
        );
        const data = await res.json();

        const datas = data.datas || [];
        const dataHoxe = new Date().toISOString().split("T")[0];

        // Se non existe, engadila
        if (!datas.includes(dataHoxe)) {
          datas.push(dataHoxe);
        }

        // PATCH actualizado
        await fetch(
          `http://localhost:8001/api/plantillas/${plantilla.id_plantilla}/`,
          {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ datas }),
          }
        );

        this.$emit("engadirPlantilla", this.plantillaSeleccionada);
        this.$emit("cargarPlantillasHoxe");
      } catch (error) {
        console.error("Erro ao engadir plantilla:", error);
        this.error = "Erro ao engadir plantilla.";
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
          :value="plantilla.nome"
          v-for="plantilla in plantillas"
          :key="plantilla"
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
</style>
