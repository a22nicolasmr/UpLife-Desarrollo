<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {};
  },
  computed: {
    id() {
      const store = useUsuarioStore();
      return store.id;
    },
  },
  methods: {
    async eliminarConta() {
      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/usuarios/${this.id}/`,
          {
            method: "DELETE",
          }
        );
        this.$emit("pecharModalEliminar");
        if (!response.ok) {
          throw new Error("Erro ao eliminar a conta.");
        }
        this.$router.push("/formularios/rexistro");
      } catch (error) {
        console.error("Erro ao subir imaxe:", error);
      }
    },
  },
};
</script>
<template>
  <div class="modal-mask">
    <div class="modal-container">
      <h1>Eliminar conta</h1>
      <div class="buttons">
        <button @click="eliminarConta()" id="pechar">Aceptar</button>
        <button @click="$emit('pecharModalEliminar')" id="cancelar">
          Cancelar
        </button>
      </div>
    </div>
  </div>
</template>
<style scoped>
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
