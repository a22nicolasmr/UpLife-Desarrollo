<script>
export default {
  data() {
    return {};
  },
  methods: {
    redirixirRexistro() {
      this.$router.push("/formularios/rexistro");
      this.$emit("pecharModal");
    },
  },
};
</script>
<template>
  <div class="modal-mask">
    <div class="modal-container">
      <h1>Pechar sesión?</h1>
      <div class="buttons">
        <button @click="redirixirRexistro()" id="pechar">Pechar</button>
        <button @click="$emit('pecharModal')" id="cancelar">Cancelar</button>
      </div>
    </div>
  </div>
</template>
<style>
.buttons {
  display: flex;
  justify-content: space-between;
}
#pechar,
#cancelar {
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

#pechar {
  background-color: red;
  color: white;
}

#cancelar {
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
@media (max-width: 768px) {
  .modal-container {
    width: 85%;
    padding: 15px 20px;
    border-radius: 10px;
  }

  .modal-container h1 {
    font-size: xx-large;
    text-align: center;
  }

  .buttons {
    margin-top: 10%;
    flex-direction: row;
    gap: 0.75rem;
    align-items: stretch;
  }

  #pechar,
  #cancelar {
    font-size: 0.9rem;
    padding: 8px 12px;
  }
}
</style>
