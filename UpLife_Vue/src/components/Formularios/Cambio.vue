<script>
export default {
  data() {
    return {
      identificador: "",
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

      if (
        !this.identificador ||
        !this.novaContrasinal ||
        !this.repetirContrasinal
      ) {
        this.erro = "Completa todos os campos";
        return;
      }

      if (this.novaContrasinal !== this.repetirContrasinal) {
        this.erro = "Os contrasinais non coinciden";
        return;
      }

      try {
        // Buscar usuario polo identificador
        const res = await fetch("http://localhost:8001/api/usuarios/");
        const usuarios = await res.json();

        const usuario = usuarios.find(
          (u) =>
            u.email === this.identificador ||
            u.nome_usuario === this.identificador
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

        if (!response.ok) throw new Error("Erro ao actualizar o contrasinal");

        this.exito = "Contrasinal cambiado con éxito";
        this.identificador = "";
        this.novaContrasinal = "";
        this.repetirContrasinal = "";
      } catch (e) {
        this.erro = "Erro ao cambiar a contrasinal.";
        console.error(e);
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
      <label for="idUsuario">Nome de usuario ou Email</label>
      <input
        type="text"
        id="idUsuario"
        v-model="identificador"
        placeholder="Escribe o nome de usuario ou email"
      />

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
