<template>
  <div class="contenedor">
    <div class="izquierda">
      <img src="/imaxes/imagen4.png" alt="imaxe inicio" />
    </div>

    <div class="derecha">
      <!-- cargar formularios -->
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "Formularios",
};
</script>

<style>
html,
body,
#app {
  height: 100%;
  width: 100%;
  margin: 0;
}

.contenedor {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.izquierda img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.izquierda,
.derecha {
  width: 50%;
  padding: 2%;
  box-sizing: border-box;
}

.izquierda {
  background-color: #e6f0ff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.derecha {
  padding: 5%;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.formulario {
  max-width: 60%;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-sizing: border-box;
}

.formulario h1 {
  font-size: xx-large;
  margin-bottom: 5%;
  color: #043133;
  font-weight: bold;
  text-align: center;
}

.formulario label {
  display: block;
  margin-bottom: 2%;
  color: #043133;
  font-weight: 500;
}

.formulario input {
  width: 100%;
  padding: 3%;
  margin-bottom: 4%;
  background-color: #eff0f2;
  border: none;
  border-radius: 4px;
  font-size: medium;
  color: #043133;
  box-sizing: border-box;
}

.formulario input::placeholder {
  color: #838383;
}

.formulario button {
  width: 100%;
  padding: 3%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: medium;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.formulario button:hover {
  background-color: #007074;
}

.formulario p {
  margin-top: 3%;
  text-align: center;
  font-size: medium;
  color: #4d5959;
}

.formulario a {
  color: #007074;
  text-decoration: none;
  font-weight: bold;
}

.formulario a:hover {
  text-decoration: underline;
}
</style>
