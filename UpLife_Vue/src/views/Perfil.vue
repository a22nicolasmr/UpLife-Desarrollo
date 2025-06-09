<script>
import Calculadora from "@/components/Perfil/Calculadora.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

import Cargando from "@/components/BarrasNavegacion/Cargando.vue";
export default {
  components: {
    Calculadora,
    Cargando,
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
      modoAplicacion: "C",
      cargando: true,
    };
  },
  computed: {
    // variables globais do id de usuario e do token
    id() {
      return useUsuarioStore().id;
    },
    token() {
      return useUsuarioStore().token;
    },
  },
  methods: {
    // actualizar datos do perfil
    async actualizarDatos() {
      if (this.id) {
        try {
          const response = await fetch(
            `https://uplife-final.onrender.com/api/usuarios/${this.id}/`,
            {
              headers: {
                Authorization: `Bearer ${this.token}`,
              },
            }
          );
          const data = await response.json();

          this.imagen =
            data.imaxe_perfil || "image/upload/v1747728142/usuario_xotela.png";
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
          this.modoAplicacion = data.modo_aplicacion || "C";

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

          store.guardarUsuarioActualizado();
        } catch (error) {
          console.error("Erro ao actualizar datos:", error);
        }
      }
    },

    //cambiar imaxe
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
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
            body: formData,
          }
        );
        const resultado = await response.json();
        console.log("Resposta do servidor:", resultado);
        await this.actualizarDatos();

        const store = useUsuarioStore();
        store.imagen =
          resultado.imaxe_perfil ||
          "image/upload/v1747728142/usuario_xotela.png";
      } catch (error) {
        console.error("Erro ao subir imaxe:", error);
      }
    },

    //actualizar modo da aplicación de non mandar correos a mandalos
    async actualizarModoAplicacion() {
      try {
        await fetch(
          `https://uplife-final.onrender.com/api/usuarios/${this.id}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify({ modo_aplicacion: this.modoAplicacion }),
          }
        );
        console.log("Modo de aplicación actualizado:", this.modoAplicacion);
        const store = useUsuarioStore();
        store.modo_aplicacion = this.modoAplicacion;
      } catch (error) {
        console.error("Erro ao actualizar modo de aplicación:", error);
      }
    },
  },

  // actualizar datos cando se monta o compoñente
  async mounted() {
    this.cargando = true;
    try {
      await this.actualizarDatos();
    } finally {
      this.cargando = false;
    }
  },
};
</script>

<template>
  <div>
    <Cargando v-if="cargando" />
    <div v-else class="container">
      <h1>Perfil</h1>
      <div class="perfil-layout">
        <div class="datos">
          <div id="divArriba">
            <div id="detallesArriba">
              <h2>Detalles da conta</h2>
              <p><strong>Nome:</strong> {{ nome }}</p>
              <p><strong>Email:</strong> {{ email }}</p>
              <p><strong>Nome de usuario:</strong> {{ nomeUsuario }}</p>
              <p>Desexa recibir notificacións das súas tarefas?</p>
              <label>
                Si:
                <input
                  type="radio"
                  name="opcion"
                  value="E"
                  v-model="modoAplicacion"
                  @change="actualizarModoAplicacion"
                />
              </label>
              <label>
                Non:
                <input
                  type="radio"
                  name="opcion"
                  value="C"
                  v-model="modoAplicacion"
                  @change="actualizarModoAplicacion"
                />
              </label>
            </div>

            <div class="imaxe-perfil">
              <img
                :src="'https://res.cloudinary.com/dkujevuxh/' + imagen"
                alt="Imaxe de usuario"
                @click="cambiarImagen()"
                tabindex="0"
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
            <button id="eliminar" @click="$emit('eliminarConta')">
              Eliminar conta
            </button>
          </div>
        </div>
        <div class="calculadora">
          <Calculadora @actualizarDatos="actualizarDatos" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#eliminar {
  background-color: red;
  color: white;
  border-radius: 3px;
  border: none;
  height: 6%;
  margin-bottom: 3%;
  margin-top: 3%;
  cursor: pointer;
}
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
  padding: 4%;
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
    gap: 0;
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
@media (min-width: 769px) and (max-width: 1370px) {
  #eliminar {
    width: 18%;
    font-size: large;
  }
  .perfil-layout {
    flex-direction: column;
    align-items: center;
    max-height: none;
    gap: 0;
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
    font-size: 1.5rem;
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
    font-size: 2rem;
  }

  h2 {
    font-size: 1.75rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }
  #divArriba {
    display: flex;
    flex-direction: column;
  }
}
</style>
