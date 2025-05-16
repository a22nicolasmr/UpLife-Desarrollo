<script>
export default {
  data() {
    return {
      identificador: "",
      erro: null,
    };
  },
  methods: {
    comprobarCodigo(event) {
      event.preventDefault();
      this.erro = null;

      const codigoCorrecto = localStorage.getItem("codigoConfirmacion");
      const correo = localStorage.getItem("correoConfirmacion");

      if (!this.identificador || this.identificador.trim() === "") {
        this.erro = "Debes introducir un código.";
        return;
      }

      if (this.identificador === codigoCorrecto) {
        // ✅ Código correcto → redirigir a cambio de contraseña
        this.$router.push({
          path: "/formularios/cambio",
          query: { email: correo },
        });
      } else {
        this.erro = "O código non é correcto. Revisa o correo.";
      }
    },
  },
};
</script>

<template>
  <div class="formulario">
    <h1>Código de confirmación</h1>

    <form @submit.prevent="comprobarCodigo">
      <label for="idUsuario">Código de cambio de contrasinal</label>
      <input
        type="text"
        id="idUsuario"
        v-model="identificador"
        placeholder="Escribe o código mandado ao correo"
      />
      <span
        >Non recibiches o código? <a @click="reenviarCodigo">Reenviar</a></span
      >

      <div v-if="erro" class="erro">{{ erro }}</div>

      <button type="submit">Enviar</button>
      <button
        type="button"
        class="cancelar"
        @click="$router.push('/formularios/inicio')"
      >
        Atrás
      </button>
    </form>
  </div>
</template>

<style scoped>
h1 {
  color: #7f5af0;
}
.erro {
  color: red;
  font-size: 0.9rem;
  margin-bottom: 8px;
}
.cancelar {
  margin-top: 10px;
  background-color: #d8d8d8;
  color: #333;
}
.cancelar:hover {
  background-color: #ccc;
}
</style>
