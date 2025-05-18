<script>
import Calculadora from "@/components/Perfil/Calculadora.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    Calculadora,
  },
  data() {
    return {
      imagen: "",
      nome: "",
      email: "",
      nomeUsuario: "",
      xenero: "",
      altura: 0,
      peso: 0,
      obxectivo: "",
      actividade: "",
      idade: 0,
      calorias: 0,
      auga: 0,
    };
  },
  computed: {
    id() {
      const store = useUsuarioStore();
      return store.id;
    },
  },
  methods: {
    // actualizar datos do usuario
    async actualizarDatos() {
      if (this.id) {
        try {
          const response = await fetch(
            `https://uplife-final.onrender.com/api/usuarios/${this.id}/`
          );
          const data = await response.json();

          // actualizar os datos no compoñente
          this.imagen = data.imaxe_perfil || "/imaxes/usuario.png";
          this.nome = data.nome;
          this.email = data.email;
          this.nomeUsuario = data.nome_usuario;
          this.xenero = data.xenero || "non especificado";
          this.altura = data.altura || "non especificado";
          this.peso = data.peso || "non especificado";
          this.obxectivo = data.obxectivo || "non especificado";
          this.actividade = data.actividade || "non especificado";
          this.idade = data.idade || "non especificado";
          this.calorias = data.calorias_diarias;
          this.auga = data.auga_diaria;

          // gardar os datos no store e en localStorage
          const store = useUsuarioStore();
          store.imagen = this.imagen;
          store.nome = this.nome;
          store.altura = this.altura;
          store.peso = this.peso;
          store.xenero = this.xenero;
          store.obxectivo = this.obxectivo;
          store.actividade = this.actividade;
          store.idade = this.idade;
          store.calorias = this.calorias;
          store.auga = this.auga;

          // gardar no localStorage
          store.guardarUsuarioActualizado();
        } catch (error) {
          console.error("Erro ao actualizar datos:", error);
        }
      }
    },

    // cambiar imaxe de usuario cando click enriba da imaxe de usuario
    cambiarImagen() {
      this.$refs.fileInput.click();
    },

    // subir nova imaxe de perfil
    async subirImagen(event) {
      const archivo = event.target.files[0];
      if (!archivo) return;

      const formData = new FormData();
      formData.append("imaxe_perfil", archivo);

      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/usuarios/${this.id}/`,
          {
            method: "PATCH",
            body: formData,
          }
        );
        const resultado = await response.json();
        this.actualizarDatos();
        const store = useUsuarioStore();
        store.imagen = resultado.imaxe_perfil || "/imaxes/usuario.png";
      } catch (error) {
        console.error("Erro ao subir imaxe:", error);
      }
    },
  },
  // actualizar datos ao montar o compoñente
  mounted() {
    this.actualizarDatos();
  },
};
</script>

<template>
  <div class="container">
    <h1>Perfil</h1>
    <div class="perfil-layout">
      <div class="datos">
        <div id="divArriba">
          <div id="detallesArriba">
            <h2>Detalles da conta</h2>
            <p><strong>Nome:</strong> {{ nome }}</p>
            <p><strong>Email:</strong> {{ email }}</p>
            <p><strong>Nome de usuario:</strong> {{ nomeUsuario }}</p>
          </div>

          <div class="imaxe-perfil">
            <img
              :src="imagen"
              alt="Imaxe de usuario"
              @click="cambiarImagen()"
            />
            <input
              type="file"
              ref="fileInput"
              style="display: none"
              @change="subirImagen"
            />
          </div>
        </div>

        <div>
          <h2>Datos do usuario</h2>
          <p><strong>Xénero:</strong> {{ xenero }}</p>
          <p>
            <strong>Altura:</strong> {{ altura
            }}<span v-if="altura !== 'non especificado'"> cm</span>
          </p>
          <p>
            <strong>Peso:</strong> {{ peso
            }}<span v-if="peso !== 'non especificado'"> kg</span>
          </p>
          <p><strong>Obxectivo:</strong> {{ obxectivo }}</p>
          <p><strong>Actividade:</strong> {{ actividade }}</p>
          <p>
            <strong>Idade:</strong> {{ idade
            }}<span v-if="idade !== 'non especificado'"> anos</span>
          </p>
          <p>
            <strong>Calorías diarias:</strong> {{ calorias
            }}<span v-if="calorias !== 'non especificado'"> kcal</span>
          </p>
          <p id="ultimoP">
            <strong>Cantidad de auga diaria:</strong> {{ auga
            }}<span v-if="auga !== 'non especificado'"> ml</span>
          </p>
        </div>
      </div>
      <div class="calculadora">
        <Calculadora @actualizarDatos="actualizarDatos" />
      </div>
    </div>
  </div>
</template>

<style scoped>
#detallesArriba > p {
  margin: 10%;
  margin-left: 0;
  margin-bottom: 0;
}
#detallesArriba {
  width: 100%;
}
#divArriba {
  display: flex;
  flex-direction: colum;
}
p {
  font-size: large;
}

h1 {
  font-size: xx-large;
  margin-bottom: 2%;
}
h2 {
  color: #7f5af0;
  font-size: x-large;
  margin: 0;
}

html,
body {
  height: 100%;
}

.container {
  background-color: #f2f2f2;
  display: flex;
  flex-direction: column;
  margin-right: 1%;
  margin-bottom: 2%;
  height: 70%;
}

.perfil-layout {
  display: flex;
  flex-direction: row;
  max-height: 80%;
  justify-content: center;
  align-items: stretch;
  gap: 0;
  margin-right: 1%;
}

.datos {
  flex: 1;
  padding: 6%;
  background-color: white;
  border-radius: 2% 0 0 2%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 2%;
}

#ultimoP {
  margin-bottom: 2%;
}

.datos p {
  margin: 6% 0;
  line-height: 20%;
}

.calculadora {
  width: 40%;
  background-color: black;
  padding: 2%;
  border-radius: 0 2% 2% 0;
  color: white;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: stretch;
}
.datos,
.calculadora {
  padding-top: 2%;
  padding-bottom: 2%;
}
.imaxe-perfil {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  margin-top: 5%;
  width: 40%;
}

.imaxe-perfil img {
  width: 15vw;
  height: 30vh;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
}
@media (max-width: 768px) {
  .perfil-layout {
    flex-direction: column;
    align-items: center;
    max-height: none;
    gap: 0; /* para que estén pegados */
  }

  .datos,
  .calculadora {
    width: 100%;
    padding: 1.5rem;
    box-sizing: border-box;
  }

  .datos {
    border-radius: 2% 2% 0 0;
  }

  .calculadora {
    background-color: #1c1c1c;
    color: white;
    border-radius: 0 0 2% 2%;
  }

  .datos p {
    font-size: 1rem;
    margin: 1rem 0;
    line-height: 1.6;
  }

  .imaxe-perfil {
    width: 100%;
    margin-top: 1rem;
  }

  .imaxe-perfil img {
    width: 50vw;
    height: auto;
  }

  h1 {
    text-align: center;
    font-size: 1.5rem;
  }

  h2 {
    font-size: 1.2rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
  #divArriba {
    display: flex;
    flex-direction: column;
  }
}
</style>
