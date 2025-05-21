<script>
export default {
  data() {
    return {
      identificador: "",
      erro: null,
    };
  },
  methods: {
    //comprobar código enviado
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
        this.$router.push({
          path: "/formularios/cambio",
          query: { email: correo },
        });
      } else {
        this.erro = "O código non é correcto. Revisa o correo.";
      }
    },
    //comprobar se o correo introducido é válido
    async reenviarCodigo(event) {
      event.preventDefault();
      this.erro = null;

      try {
        const correo = localStorage.getItem("correoConfirmacion"); // 🔁 Recuperar o correo anterior

        if (!correo) {
          this.erro = "Non hai ningún correo gardado para reenviar.";
          return;
        }

        const codigo = Math.floor(100000 + Math.random() * 900000).toString();

        localStorage.setItem("codigoConfirmacion", codigo); // 🔁 Só actualizamos o código, o correo xa está

        const envio = await fetch(
          "https://uplife-final.onrender.com/enviar-codigo/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: correo,
              codigo: codigo,
            }),
          }
        );

        if (!envio.ok) {
          this.erro = "Erro ao reenviar o correo.";
          return;
        }

        this.$router.push("/formularios/codigo");
      } catch (error) {
        console.error("Erro:", error);
        this.erro = "Erro de conexión. Inténtao máis tarde.";
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
a {
  cursor: pointer;
}
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
