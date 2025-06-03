<script>
export default {
  data() {
    return {
      modal: false,
      menuAbierto: false,
    };
  },
  computed: {
    //obter ruta actual
    rutaActual() {
      return this.$route.path;
    },

    //comprobar se se está accedendo dende un móvil
    esMovil() {
      return window.innerWidth <= 768;
    },
  },

  //engadir o evento resize cando se monta o compoñente e quitalo cando se desmonta
  mounted() {
    window.addEventListener("resize", this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    //abrir e pechar menú de hamburguesa en función de se se está en móvil ou non
    handleResize() {
      if (!this.esMovil && this.menuAbierto) {
        this.menuAbierto = false;
      }
    },
  },
};
</script>

<template>
  <div>
    <div class="hamburguesa" @click="menuAbierto = !menuAbierto">
      <a href="#">☰</a>
    </div>

    <nav :class="{ abierto: menuAbierto }" v-if="menuAbierto || !esMovil">
      <div class="menu-superior">
        <ul>
          <li>
            <img
              src="/imaxes/Logo.PNG"
              alt="UpLife"
              @click="$router.push('/formularios/rexistro')"
            />
          </li>
          <li
            :class="{ activo: rutaActual === '/tarefas' }"
            @click="$router.push('/tarefas')"
          >
            <a href="#">Tarefas</a>
          </li>
          <li
            :class="{ activo: rutaActual === '/exercicios' }"
            @click="$router.push('/exercicios')"
          >
            <a href="#">Exercicios</a>
          </li>
          <li
            :class="{ activo: rutaActual === '/comidas' }"
            @click="$router.push('/comidas')"
          >
            <a href="#">Comidas</a>
          </li>
          <li
            :class="{ activo: rutaActual === '/plantillas' }"
            @click="$router.push('/plantillas')"
          >
            <a href="#">Plantillas</a>
          </li>
          <li
            :class="{ activo: rutaActual === '/auga' }"
            @click="$router.push('/auga')"
          >
            <a href="#">Auga</a>
          </li>
          <li
            :class="{ activo: rutaActual === '/medallas' }"
            @click="$router.push('/medallas')"
          >
            <a href="#">Medallas</a>
          </li>
        </ul>
      </div>

      <div class="menu-inferior">
        <hr />
        <ul>
          <li
            :class="{ activo: rutaActual === '/perfil' }"
            @click="$router.push('/perfil')"
          >
            <a href="#">Perfil</a>
          </li>
          <li
            :class="{ activo: rutaActual === '/formularios/rexistro' }"
            @click="$emit('toggleModal')"
          >
            <a href="#">Pechar sesión</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}
nav {
  background-color: white;
  padding: 1% 1%;
  display: flex;
  flex-direction: column;
  height: 98%;
  border-right: 1px solid #ccc;
  position: fixed;
  width: 10%;
  transition: transform 0.3s ease;
}

.menu-superior {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  font-size: large;
}

.menu-inferior {
  display: flex;
  flex-direction: column;
  margin-top: auto;
  font-size: large;
  margin-bottom: 6%;
}

ul {
  list-style: none;
  padding: 0%;
  margin: 0%;
  display: flex;
  flex-direction: column;
  gap: 2%;
  justify-content: center;
  align-items: center;
}

li {
  padding: 5%;
  color: black;
  cursor: pointer;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  transition: background-color 0.3s;
}
img {
  height: 100%;
  width: 100%;
}
li.activo {
  color: white;
  background-color: #4880ff;
  padding-left: 20%;
  padding-right: 20%;
}

hr {
  margin: 10% 0;
  border: none;
  border-top: 1px solid #ccc;
}

.hamburguesa {
  display: none;
  font-size: 2rem;
  cursor: pointer;
  padding: 1rem;
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 10000;
}

@media (max-width: 768px) {
  nav {
    width: 35%;
    height: 100%;
    top: 0;
    left: 0;
    position: fixed;
    z-index: 9999;
    padding-top: 20%;
    transform: translateX(-100%);
  }

  nav.abierto {
    transform: translateX(0);
  }

  .hamburguesa {
    display: block;
    top: -1.5%;
  }

  .menu-superior {
    flex-grow: 0;
    margin-bottom: 90%;
  }

  .menu-superior ul,
  .menu-inferior ul {
    gap: 2%;
  }

  .menu-superior li,
  .menu-inferior li {
    padding: 0.4rem 0.6rem;
    font-size: medium;
  }

  .menu-inferior {
    margin-top: 100%;
  }

  li.activo {
    padding-left: 0.6rem;
    padding-right: 0.6rem;
  }

  hr {
    margin: 0.5rem 0;
  }
}
@media (min-width: 769px) and (max-width: 1370px) {
  nav {
    width: 20%;
    height: 100%;
    top: 0;
    left: 0;
    position: fixed;
    z-index: 9999;
    padding-top: 20%;
    transform: translateX(-100%);
  }

  nav.abierto {
    transform: translateX(0);
  }

  .hamburguesa {
    display: block;
    top: -1.4%;
    font-size: 2.5em;
  }

  .menu-superior {
    flex-grow: 0;
    margin-bottom: 30%;
  }

  .menu-superior ul,
  .menu-inferior ul {
    gap: 2%;
  }

  .menu-superior li,
  .menu-inferior li {
    padding: 0.4rem 0.6rem;
    font-size: larger;
  }

  .menu-inferior {
    margin-top: 100%;
  }

  li.activo {
    padding-left: 0.6rem;
    padding-right: 0.6rem;
  }

  hr {
    margin: 0.5rem 0;
  }
}
</style>
