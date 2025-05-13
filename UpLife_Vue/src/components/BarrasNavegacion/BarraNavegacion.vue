<script>
export default {
  data() {
    return {
      modal: false,
    };
  },

  // cambiar ruta actual segun onde se atope o usuario
  computed: {
    rutaActual() {
      return this.$route.path;
    },
  },
  methods: {},
};
</script>

<template>
  <!-- reidirixir usuario segun onde pulse -->
  <nav>
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
          Tarefas
        </li>
        <li
          :class="{ activo: rutaActual === '/exercicios' }"
          @click="$router.push('/exercicios')"
        >
          Exercicios
        </li>
        <li
          :class="{ activo: rutaActual === '/comidas' }"
          @click="$router.push('/comidas')"
        >
          Comidas
        </li>
        <li
          :class="{ activo: rutaActual === '/plantillas' }"
          @click="$router.push('/plantillas')"
        >
          Plantillas
        </li>
        <li
          :class="{ activo: rutaActual === '/auga' }"
          @click="$router.push('/auga')"
        >
          Auga
        </li>
        <li
          :class="{ activo: rutaActual === '/medallas' }"
          @click="$router.push('/medallas')"
        >
          Medallas
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
          Perfil
        </li>
        <li
          :class="{ activo: rutaActual === '/formularios/rexistro' }"
          @click="$emit('toggleModal')"
        >
          Pechar sesión
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
nav {
  background-color: white;
  padding: 1% 1%;
  display: flex;
  flex-direction: column;
  height: 98%;
  border-right: 1px solid #ccc;
  position: fixed;
  width: 10%;
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
</style>
