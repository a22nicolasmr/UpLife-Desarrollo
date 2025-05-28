<script>
export default {
  data() {
    return {
      novaContrasinal: "",
      repetirContrasinal: "",
      erro: "",
      exito: "",
    };
  },
  methods: {
    //cambiar contrasinal
    async cambiarContrasinal() {
      this.erro = "";
      this.exito = "";

      if (!this.novaContrasinal || !this.repetirContrasinal) {
        this.erro = "Completa todos os campos.";
        return;
      }

      if (this.novaContrasinal !== this.repetirContrasinal) {
        this.erro = "Os contrasinais non coinciden.";
        return;
      }

      const correo = localStorage.getItem("correoConfirmacion");
      if (!correo) {
        this.erro = "Non se atopou o correo do usuario.";
        return;
      }

      try {
        const res = await fetch(
          "https://uplife-final.onrender.com/obter-usuario-id/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: correo }),
          }
        );

        const data = await res.json();

        if (!res.ok || !data.id_usuario) {
          this.erro = "Usuario non atopado.";
          return;
        }

        const response = await fetch(
          `https://uplife-final.onrender.com/api/usuarios/${data.id_usuario}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              contrasinal: this.novaContrasinal,
            }),
          }
        );

        if (!response.ok) throw new Error("Erro ao actualizar o contrasinal.");

        this.exito = "Contrasinal cambiado con éxito.";
        this.novaContrasinal = "";
        this.repetirContrasinal = "";

        //borrar do storage o correo e o código
        localStorage.removeItem("correoConfirmacion");
        localStorage.removeItem("codigoConfirmacion");

        setTimeout(() => {
          this.$router.push("/formularios/inicio");
        }, 2000);
      } catch (e) {
        console.error(e);
        this.erro = "Erro ao cambiar a contrasinal.";
      }
    },

    //cambiar vista a inicio
    cancelar() {
      this.$router.push("/formularios/inicio");
    },
  },
};
</script>

<template>
  <div class="formulario">
    <h1>Cambiar Contrasinal</h1>

    <form @submit.prevent="cambiarContrasinal">
      <label for="nova">Novo Contrasinal</label>
      <input
        type="password"
        id="nova"
        v-model="novaContrasinal"
        placeholder="Escribe o novo contrasinal"
      />

      <label for="repetir">Repite o Contrasinal</label>
      <input
        type="password"
        id="repetir"
        v-model="repetirContrasinal"
        placeholder="Repite o novo contrasinal"
      />

      <div v-if="erro" class="erro">{{ erro }}</div>
      <div v-if="exito" class="exito">{{ exito }}</div>

      <button type="submit">Gardar cambios</button>
      <button type="button" class="cancelar" @click="cancelar">Atrás</button>
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
.exito {
  color: green;
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
