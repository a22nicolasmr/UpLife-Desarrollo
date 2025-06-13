<template>
  <div class="modal-mask">
    <div class="modal-container"></div>
    <div class="guia-wrapper">
      <div class="guia-container">
        <button @click="$emit('pecharUso')">X</button>
        <h1>Guía de Uso de UpLife</h1>
        <p class="intro">
          Comeza configurando os teus datos persoais para que a app poida
          calcular as túas necesidades diarias.
        </p>

        <section>
          <h2>1. Completa o teu perfil</h2>
          <ul>
            <li>Vai á sección <strong>Perfil</strong>.</li>
            <li>
              Engade o teu peso, altura, idade, nivel de actividade e outros
              datos relevantes.
            </li>
            <li>
              O sistema calculará as túas calorías e inxesta de auga diaria
              recomendadas.
            </li>
          </ul>
        </section>

        <section>
          <h2>2. Activar recordatorios por correo</h2>
          <ul>
            <li>
              Na sección de Perfil, activa a opción para recibir
              <strong>notificacións por correo electrónico</strong>.
            </li>
            <li>
              Estas alertas avisaranche cando se aproxime a hora de realizar
              unha tarefa.
            </li>
          </ul>
        </section>
        <section>
          <h2>3. Cambiar a foto de perfil</h2>
          <ul>
            <li>
              Podes cambiar a túa foto de perfil facendo click na fotografía que
              hai no apartado de Perfil.
            </li>
          </ul>
        </section>
        <section>
          <h2>4. Comeza a usar a aplicación</h2>
          <ul>
            <li>Engade tarefas, rexistra comidas, hidratación e exercicios.</li>
            <li>Recibirás medallas e seguirás o teu progreso diariamente.</li>
          </ul>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.guia-wrapper {
  height: 100vh;
  width: 100vw;
  background-color: #f2f2f2;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-y: auto;
  padding: 20px;
}

.guia-container {
  width: 90%;
  max-width: 850px;
  background-color: white;
  color: #1c1c1c;
  border-radius: 16px;
  padding: 4vh 5vw;
  box-shadow: 0 0 14px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  max-height: 95vh;
  position: relative;
}

.guia-container > button {
  position: absolute;
  top: 15px;
  right: 15px;
  background-color: #e53e3e;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 1.2rem;
  cursor: pointer;
  font-weight: bold;
  line-height: 1;
  transition: background-color 0.2s ease;
}

.guia-container > button:hover {
  background-color: #c53030;
}
</style>
