<script>
import axios from "axios";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      email: "",
      contrasinal: "",
      erro: "",
    };
  },
  methods: {
    // mandar formulario se os datos estan correctos
    async mandarFormulario() {
      this.erro = "";

      if (!this.email || !this.contrasinal) {
        this.erro = "Completa todos os campos";
        this.contrasinal = "";
        return;
      }

      // accede a login donde se fai validación dos campos
      try {
        const response = await axios.post("http://localhost:8001/login/", {
          identificador: this.email,
          contrasinal: this.contrasinal,
        });

        if (response.status === 200) {
          const usuarioStore = useUsuarioStore();
          await usuarioStore.cargarUsuario(this.email);
          await usuarioStore.actualizarDatos();

          // redirixese a ruta desexada mandando como query o nome do usuario
          this.$router.push({
            name: "tarefas",
            query: { nome: this.email },
          });
        }
      } catch (error) {
        console.error("Erro ao iniciar sesión:", error);
        if (error.response?.status === 401 || error.response?.status === 404) {
          this.erro = "Nome de usuario ou contrasinal incorrecto";
        } else {
          this.erro = "Erro ao iniciar sesión. Inténtao de novo";
        }
        this.contrasinal = "";
      }
    },
  },
};
</script>

<template>
  <div class="formulario">
    <h1>Benvido de volta a UpLife</h1>
    <form action="" method="get">
      <label for="inputEmail">Nome de usuario ou Email</label>
      <input
        type="text"
        id="inputEmail"
        placeholder="Escribe o teu nome de usuario ou email"
        v-model="email"
      />

      <label for="inputContrasinal">Contrasinal</label>
      <input
        type="password"
        id="inputContrasinal"
        placeholder="Escribe o teu contrasinal"
        v-model="contrasinal"
      />
      <div class="recuperar-contrasinal">
        <span>Esquecíches o teu contrasinal?</span>
        <a @click.prevent="$router.push('/formularios/cambio')">Recuperar</a>
      </div>
      <div v-if="erro" class="erro">
        {{ erro }}
      </div>

      <button type="submit" @click.prevent="mandarFormulario()">
        Iniciar sesión
      </button>

      <p>
        Non tes unha conta?
        <a href="#" @click.prevent="$router.push({ name: 'rexistro' })">
          Rexistro
        </a>
      </p>
    </form>
  </div>
</template>

<style scoped>
.erro {
  color: red;
  font-size: 0.9rem;
  margin-bottom: 1%;
}
.recuperar-contrasinal {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  font-size: 0.9rem;
  margin: 6px 0 12px;
  gap: 6px;
}

.recuperar-contrasinal a {
  cursor: pointer;
}
</style>
