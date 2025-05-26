<script setup>
import { useUsuarioStore } from "@/stores/useUsuario";
import { onMounted, watch } from "vue";
import { useRoute } from "vue-router";

const usuarioStore = useUsuarioStore();
const route = useRoute();

watch(
  // cargar novo nome de usuario
  () => route.query.nome,
  (novoNome) => {
    if (novoNome) {
      usuarioStore.cargarToken(); // cargar token primeiro
      usuarioStore.cargarUsuario(novoNome);
    }
  },
  { immediate: true }
);
</script>

<template>
  <div class="barra-superior">
    <div class="usuario-info">
      <img
        :src="'https://res.cloudinary.com/dkujevuxh/' + usuarioStore.imagen"
        alt="Usuario"
        class="usuario-imagen"
      />
      <div class="usuario-detalles">
        <div class="usuario-nombre" @click="$router.push('/perfil')">
          {{ usuarioStore.nome }}
        </div>
        <div class="usuario-medallas" @click="$router.push('/medallas')">
          {{ usuarioStore.medallas }} Medallas
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.barra-superior {
  background-color: #4880ff;
  padding: 0.5%;
  color: white;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  position: fixed;
  top: 0;
  width: 100%;
}

.usuario-info {
  display: flex;
  align-items: center;
  margin-right: 3%;
}

.usuario-imagen {
  width: 7vh;
  height: 7vh;
  border-radius: 50%;
  margin-right: 2vh;
  cursor: pointer;
}

.usuario-detalles {
  display: flex;
  flex-direction: column;
  justify-content: center;
  cursor: pointer;
}

.usuario-nombre {
  font-weight: bold;
}

.usuario-medallas {
  font-size: 2vh;
  color: #d8d8d8;
}
@media (max-width: 768px) {
  .barra-superior {
    padding: 0.4rem 0.8rem;
    height: auto;
  }

  .usuario-info {
    margin-right: 15%;
  }

  .usuario-imagen {
    width: 5vh;
    height: 5vh;
    margin-right: 1vh;
  }

  .usuario-nombre {
    font-size: 0.9rem;
  }

  .usuario-medallas {
    font-size: 0.75rem;
  }
}
</style>
