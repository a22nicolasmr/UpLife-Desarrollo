<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  props: {
    tarefaActual: Object,
  },
  data() {
    return {};
  },
  methods: {
    // establecer a hora da tarefa 10 minutos despois da hora indicada inicialmente
    async posporTarefa() {
      try {
        const usuarioStore = useUsuarioStore();
        usuarioStore.cargarToken(); // asegurar que o token está cargado
        const token = usuarioStore.token;

        const [horas, minutos] = this.tarefaActual.hora.split(":").map(Number);
        const tarefaDate = new Date();
        tarefaDate.setHours(horas, minutos + 10);

        const novaHora = tarefaDate.toTimeString().slice(0, 5);

        const payload = {
          hora: novaHora,
        };

        const response = await fetch(
          `https://uplife-final.onrender.com/api/tarefas/${this.tarefaActual.id_tarefa}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) throw new Error("erro ao pospor tarefa");

        window.location.reload();
      } catch (error) {
        console.error("erro ao pospor tarefa:", error);
      }
    },
  },
};
</script>

<template>
  <div class="modal-mask">
    <div class="modal-container">
      <h1>{{ tarefaActual.hora }}</h1>
      <h1>{{ tarefaActual.titulo }}</h1>
      <div class="buttons">
        <button @click="$emit('cerrarAviso')" id="aceptar">Aceptar</button>
        <button id="posponher" @click="posporTarefa">Pospor 10 minutos</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.buttons {
  display: flex;
  justify-content: space-between;
}
#posponher,
#aceptar {
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

#posponher {
  background-color: lightgrey;
  color: white;
}

#aceptar {
  background-color: #4880ff;
  color: white;
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
}
.modal-container {
  width: 300px;
  margin: auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}
</style>
