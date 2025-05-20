<script>
export default {
  data() {
    return {
      identificador: "",
      erro: null,
    };
  },
  methods: {
    // getCookie(name) {
    //   let cookieValue = null;
    //   if (document.cookie && document.cookie !== "") {
    //     const cookies = document.cookie.split(";");
    //     for (let i = 0; i < cookies.length; i++) {
    //       const cookie = cookies[i].trim();
    //       if (cookie.startsWith(name + "=")) {
    //         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //         break;
    //       }
    //     }
    //   }
    //   return cookieValue;
    // },

    //comprobar se o correo introducido é válido
    async comprobarCorreo(event) {
      event.preventDefault();
      this.erro = null;

      const esEmailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
        this.identificador
      );
      if (!esEmailValido) {
        this.erro = "Introduce un correo electrónico válido.";
        return;
      }

      try {
        const res = await fetch(
          "https://uplife-final.onrender.com/api/usuarios/"
        );
        if (!res.ok) throw new Error("Error al acceder a usuarios");
        const usuarios = await res.json();

        const existe = usuarios.some(
          (u) => u.email.toLowerCase() === this.identificador.toLowerCase()
        );

        if (!existe) {
          this.erro = "Este correo no está registrado.";
          return;
        }

        const codigo = Math.floor(100000 + Math.random() * 900000).toString();

        localStorage.setItem("correoConfirmacion", this.identificador);
        localStorage.setItem("codigoConfirmacion", codigo);

        const envio = await fetch(
          "https://uplife-final.onrender.com/enviar-codigo/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            // "X-CSRFToken": getCookie("csrftoken"),
            body: JSON.stringify({
              email: this.identificador,
              codigo: codigo,
            }),
          }
        );

        if (!envio.ok) {
          this.erro = "Error al enviar el correo.";
          return;
        }

        this.$router.push("/formularios/codigo");
      } catch (error) {
        console.error("Error:", error);
        this.erro = "Error de conexión. Inténtalo más tarde.";
      }
    },
  },
};
</script>

<template>
  <div class="formulario">
    <h1>Código electrónico</h1>

    <form @submit.prevent="comprobarCorreo">
      <label for="idUsuario">Correo electrónico</label>
      <input
        type="text"
        id="idUsuario"
        v-model="identificador"
        placeholder="Correo electrónico"
      />

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
