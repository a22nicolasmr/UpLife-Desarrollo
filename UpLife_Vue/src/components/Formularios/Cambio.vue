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
        const res = await fetch("http://localhost:8001/api/usuarios/");
        const usuarios = await res.json();

        const usuario = usuarios.find(
          (u) => u.email.toLowerCase() === correo.toLowerCase()
        );

        if (!usuario) {
          this.erro = "Usuario non atopado.";
          return;
        }

        const response = await fetch(
          `http://localhost:8001/api/usuarios/${usuario.id_usuario}/`,
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

        // Limpia el localStorage por seguridade
        localStorage.removeItem("correoConfirmacion");
        localStorage.removeItem("codigoConfirmacion");

        // Redirige tras 2 segundos
        setTimeout(() => {
          this.$router.push("/formularios/inicio");
        }, 2000);
      } catch (e) {
        console.error(e);
        this.erro = "Erro ao cambiar a contrasinal.";
      }
    },

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
