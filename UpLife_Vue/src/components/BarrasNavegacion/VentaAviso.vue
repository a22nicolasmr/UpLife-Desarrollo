<script>
export default {
  props: {
    tarefaActual: Object,
  },
  data() {
    return {};
  },
  mounted() {},
  methods: {
    async posporTarefa() {
      try {
        const [horas, minutos] = this.tarefaActual.hora.split(":").map(Number);
        const tarefaDate = new Date();
        tarefaDate.setHours(horas, minutos + 10);

        const novaHora = tarefaDate.toTimeString().slice(0, 5);

        const payload = {
          hora: novaHora,
        };

        const response = await fetch(
          `http://localhost:8001/api/tarefas/${this.tarefaActual.id_tarefa}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) throw new Error("Erro ao pospor tarefa");

        console.log("Tarefa posposta:", await response.json());
        window.location.reload();
      } catch (error) {
        console.error("Erro ao pospor tarefa:", error);
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
<style>
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
