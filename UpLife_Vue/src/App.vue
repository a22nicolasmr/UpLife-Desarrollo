<script>
import BarraNavegacion from "./components/BarrasNavegacion/BarraNavegacion.vue";
import BarraSuperior from "./components/BarrasNavegacion/BarraSuperior.vue";
import VentaAviso from "./components/BarrasNavegacion/VentaAviso.vue";
import VentaEliminar from "./components/BarrasNavegacion/VentaEliminar.vue";
import VentaPechar from "./components/BarrasNavegacion/VentaPechar.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      modalActivo: false,
      avisoActivo: false,
      tarefasConHora: [],
      tarefaActual: null,
      intervalId: null,
      valorMedallas: [],
      ventaEliminar: false,
    };
  },
  components: {
    BarraNavegacion,
    BarraSuperior,
    VentaPechar,
    VentaAviso,
    VentaEliminar,
  },
  methods: {
    // coller o valor das rachas para enviar a clase Medallas como prop
    mandarRachas(valorMedallas) {
      this.valorMedallas = valorMedallas;
    },
    // activar/desactivar modal pechar sesión
    toggleModal() {
      this.modalActivo = !this.modalActivo;
    },
    // coller tarefas con hora filtrando por as que non foran notificadas previamente
    emitirDatasConTarefas(tarefas) {
      this.tarefasConHora = tarefas.map((t) => ({ ...t, notificada: false }));
    },

    // comprobar se a hora dunha tarefa coincide coa hora actual
    // true = abrir ventá aviso
    comprobarHoras() {
      const agora = new Date();
      const horaActual = agora.toTimeString().slice(0, 5);

      for (const tarefa of this.tarefasConHora) {
        if (
          tarefa.hora &&
          tarefa.hora.slice(0, 5) === horaActual &&
          !tarefa.notificada &&
          !tarefa.completada
        ) {
          this.tarefaActual = tarefa;
          this.avisoActivo = true;
          tarefa.notificada = true;
          return;
        }
      }
    },
    // pechar ventá aviso
    cerrarAviso() {
      this.avisoActivo = false;
      this.tarefaActual = null;
    },

    // abrir modal para eliminar conta
    async eliminarConta() {
      this.ventaEliminar = true;
    },

    pecharModalEliminar() {
      this.ventaEliminar = false;
    },
  },
  watch: {
    // se o aviso está activo , o son de ventá aviso execútase en bucle
    avisoActivo(novoValor) {
      const audio = this.$refs.audioAviso;
      if (audio) {
        if (novoValor) {
          audio.loop = true;
          audio.play();
        } else {
          audio.pause();
          audio.currentTime = 0;
        }
      }
    },
  },

  computed: {
    // cambiar según a ruta na que se atope o usuario
    rutaActual() {
      return this.$route.path;
    },

    // mostrar as barras de navegación en todas as pantaias menos nas pantaias listadas no método
    mostrarBarra() {
      return (
        this.$route.path !== "/formularios/rexistro" &&
        this.$route.path !== "/formularios/inicio" &&
        this.$route.path !== "/condicions" &&
        this.$route.path !== "/formularios/cambio" &&
        this.$route.path !== "/formularios/codigo" &&
        this.$route.path !== "/formularios/correoCodigo"
      );
    },

    // devolver nome do usuario actual
    nombreUsuario() {
      return this.$route.query.nome;
    },
    id() {
      const store = useUsuarioStore();
      return store.id;
    },
  },
  mounted() {
    // cando se monta a aplicación , cargar o usuario
    const usuarioStore = useUsuarioStore();
    usuarioStore.cargarDesdeStorage();

    // se non hai id de usuario e nome de usuario redirixir ao formulario de inicio
    if (!usuarioStore.id || !usuarioStore.nome) {
      this.$router.push("/formularios/inicio");
    }

    // executar comprobación hora cada segundo
    this.intervalId = setInterval(this.comprobarHoras, 1000);
    // this.intervalId = setInterval(this.comprobarHoras, 5000);
  },
  // quitar o intervalo para que non siga comprobando unha vez desmontado o compoñente
  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
};
</script>

<template>
  <div class="layout">
    <audio ref="audioAviso" src="/audio/alarma.mp3"></audio>
    <div v-if="mostrarBarra" class="barra-superior">
      <BarraSuperior
        v-if="mostrarBarra"
        :nome="nombreUsuario"
        :key="nombreUsuario"
      />
    </div>
    <div class="barra-navegacion">
      <BarraNavegacion
        v-if="mostrarBarra"
        :rutaActual="rutaActual"
        @toggleModal="toggleModal"
      />
    </div>

    <div :class="['vista', { 'sin-barras': !mostrarBarra }]">
      <router-view
        @mandarRachas="mandarRachas"
        :valorMedallas="valorMedallas"
        @emitirDatasConTarefas="emitirDatasConTarefas"
        @eliminarConta="eliminarConta"
      />
    </div>

    <VentaPechar v-show="modalActivo" @pecharModal="toggleModal" />
    <VentaAviso
      v-if="avisoActivo && tarefaActual"
      :tarefaActual="tarefaActual"
      @cerrarAviso="cerrarAviso"
    />
    <VentaEliminar
      v-if="ventaEliminar"
      @pecharModalEliminar="pecharModalEliminar"
    >
    </VentaEliminar>
  </div>
</template>

<style>
/* import de fuente nunito sans */
@import url("https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,wght@0,200;0,300;0,400;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,600;1,700;1,800;1,900&display=swap");
html,
body,
#app {
  height: 100%;
  margin: 0;
}

.barra-superior {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  z-index: 1000;
}
.barra-navegacion {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  z-index: 1000;
}

body {
  margin: 0;
  height: 100%;
  width: 100%;

  background-color: #eff0f2;
}
* {
  font-family: "Nunito Sans", sans-serif !important;
}

.layout {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  width: 100%;
}

.vista {
  flex: 1;
  margin-top: 4%;
  margin-left: 16%;
  overflow-y: hidden;
  min-height: 0;
}

.sin-barras {
  margin: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
}
@media (max-width: 768px) {
  .vista {
    margin: 0;
    margin-top: 8%;
    margin-right: 5%;
    padding: 3%;
    width: 94%;
    overflow-y: auto;
  }

  .layout {
    margin: 0;
    padding: 0;
    width: 100vw;
    min-height: 100vh;
  }

  .sin-barras {
    width: 100vw !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
  }
}
</style>
