<script setup>
// uso de script setup para un compoñente mais simple e rápido
import { useRouter } from "vue-router";

const router = useRouter();

function aceptarTerminos() {
  router.push("/formularios/rexistro");
}
</script>

<template>
  <div class="terminos-wrapper">
    <div class="terminos-container">
      <h1>Termos e Condicións de Uso</h1>

      <p class="intro">
        A protección da túa información persoal é unha prioridade para nós. Ao
        crear unha conta, aceptas as seguintes condicións legais que garantizan
        transparencia, seguridade e conformidade coas normativas vixentes.
      </p>

      <section>
        <h2>Regulamento Xeral de Protección de Datos (RXPD / GDPR)</h2>
        <ul>
          <li>
            Solicitude de <strong>consentimento expreso</strong> para o
            tratamento dos teus datos.
          </li>
          <li>
            Dereito de
            <strong>acceso, rectificación, cancelación e oposición</strong>
            (ARCO).
          </li>
          <li>
            Información clara sobre o uso de <strong>cookies</strong> e
            políticas de privacidade.
          </li>
        </ul>
        <p>
          Máis información:
          <a
            href="https://www.boe.es/doue/2016/119/L00001-00088.pdf"
            target="_blank"
            rel="noopener noreferrer"
          >
            Regulamento (UE) 2016/679 (BOE)
          </a>
        </p>
      </section>

      <section>
        <h2>Lei de Servizos da Sociedade da Información (LSSI-CE)</h2>
        <ul>
          <li>
            Información visible sobre o <strong>responsable da web</strong> e os
            seus datos de contacto.
          </li>
          <li>
            Inclusión de <strong>aviso legal</strong> e política de privacidade.
          </li>
          <li>
            Xestión adecuada de <strong>cookies</strong> segundo a normativa.
          </li>
        </ul>
        <p>
          Máis información:
          <a
            href="https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758"
            target="_blank"
            rel="noopener noreferrer"
          >
            LSSI-CE (BOE)
          </a>
        </p>
      </section>

      <section>
        <h2>Compromisos do Usuario</h2>
        <ul>
          <li>
            A información proporcionada debe ser veraz, completa e actualizada.
          </li>
          <li>
            Non se permite o uso fraudulento nin o acceso indebido á conta
            doutra persoa.
          </li>
          <li>
            O usuario comprométese a manter a confidencialidade das súas
            credenciais.
          </li>
        </ul>
      </section>

      <button @click="aceptarTerminos">Aceptar</button>
    </div>
  </div>
</template>

<style scoped>
.terminos-wrapper {
  height: 100vh;
  width: 100vw;
  background-color: #f2f2f2;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-y: auto;
}

.terminos-container {
  width: 90%;
  max-width: 850px;
  background-color: white;
  color: #1c1c1c;
  border-radius: 16px;
  padding: 4vh 5vw;
  box-shadow: 0 0 14px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  max-height: 95vh;
}

h1 {
  text-align: center;
  color: #7f5af0;
  font-size: 2rem;
  margin-bottom: 2vh;
}

.intro {
  margin-bottom: 3vh;
  font-size: 1.05rem;
  color: #444;
}

h2 {
  color: #333;
  margin-top: 2vh;
  margin-bottom: 1vh;
  font-size: 1.2rem;
}

ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-bottom: 1.5vh;
}

li {
  margin-bottom: 0.6rem;
}

a {
  color: #4880ff;
  text-decoration: underline;
}

button {
  display: block;
  margin: 4vh auto 0;
  background-color: #4880ff;
  color: white;
  padding: 1vh 2.5vw;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #684bd6;
}
@media (max-width: 768px) {
  .terminos-container {
    width: 95%;
    padding: 6vh 6vw;
    max-height: 100vh;
    border-radius: 12px;
    box-shadow: none;
    font-size: 0.95rem;
  }

  h1 {
    font-size: 1.5rem;
    margin-bottom: 2vh;
  }

  h2 {
    font-size: 1.1rem;
    margin-top: 1.5vh;
    margin-bottom: 1vh;
  }

  .intro {
    font-size: 1rem;
  }

  ul {
    padding-left: 1.2rem;
    margin-bottom: 1.5vh;
  }

  li {
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
  }

  button {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    margin-top: 3vh;
  }
}
@media (min-width: 769px) and (max-width: 1370px) {
  .terminos-container {
    width: 95%;
    padding: 6vh 6vw;
    max-height: 100vh;
    border-radius: 12px;
    box-shadow: none;
    font-size: 0.95rem;
  }

  h1 {
    font-size: 1.5rem;
    margin-bottom: 2vh;
  }

  h2 {
    font-size: 1.1rem;
    margin-top: 1.5vh;
    margin-bottom: 1vh;
  }

  .intro {
    font-size: 1rem;
  }

  ul {
    padding-left: 1.2rem;
    margin-bottom: 1.5vh;
  }

  li {
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
  }

  button {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    margin-top: 3vh;
  }
}
</style>
