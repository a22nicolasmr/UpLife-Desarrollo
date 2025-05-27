<template>
  <div class="not-found">
    <div class="animation">
      <h1 class="bounce">404</h1>
      <p class="fade-in">Páxina non atopada</p>
      <router-link to="/" class="volver">⬅ Volver ao inicio</router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  min-height: 100vh;
  text-align: center;
  background-color: #f0f2f5;
  box-sizing: border-box;
}

.animation h1 {
  font-size: 9rem;
  margin: 0;
  color: #4880ff;
  animation: bounce 1s infinite alternate;
}

.animation p {
  font-size: 1.5rem;
  color: #333;
  animation: fadeIn 2s ease-in-out;
  margin-top: 0.5rem;
}

.volver {
  margin-top: 1.5rem;
  display: inline-block;
  text-decoration: none;
  color: #4880ff;
  font-weight: bold;
  font-size: 1rem;
  border: 2px solid #4880ff;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.3s, color 0.3s;
}

.volver:hover {
  background-color: #4880ff;
  color: white;
}

@keyframes bounce {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-20px);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .animation h1 {
    font-size: 5rem;
  }

  .animation p {
    font-size: 1.1rem;
  }

  .volver {
    font-size: 0.9rem;
    padding: 0.4rem 0.8rem;
  }
}
</style>
