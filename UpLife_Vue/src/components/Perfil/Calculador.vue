<script>
export default {
  emits: ["updateAltura", "updatePeso"],
  data() {
    return {
      altura: 170,
      peso: 72,
    };
  },
  watch: {
    //obter novos valores de altura
    altura(nuevaAltura) {
      this.$emit("updateAltura", nuevaAltura);
    },

    //obter novos valores de peso
    peso(nuevoPeso) {
      this.$emit("updatePeso", nuevoPeso);
    },
  },
  computed: {
    //calcular imc cos datos introducidos
    imc() {
      const alturaM = this.altura / 100;
      return this.peso / (alturaM * alturaM);
    },

    //determinar estado do imc en función do valor calculado
    estadoIMC() {
      const v = this.imc;
      if (v < 18.5) return "Baixo peso";
      if (v < 25) return "Saudable";
      if (v < 30) return "Sobrepeso";
      return "Obesidade";
    },
  },
  methods: {
    //calcular posición dos sliders
    calcularPosicion() {
      const min = 10;
      const max = 40;
      const imc = this.imc;
      const percent = ((imc - min) / (max - min)) * 100;
      return Math.min(100, Math.max(0, percent));
    },
  },
};
</script>

<template>
  <div class="imc-wrapper">
    <div class="inputs">
      <div class="input-box altura">
        <label>Altura</label>
        <div class="range-control">
          <button @click="altura = Math.max(100, altura - 1)">−</button>
          <input
            type="range"
            min="100"
            max="220"
            :value="altura"
            @input="(e) => (altura = Number(e.target.value))"
          />
          <button @click="altura = Math.min(220, altura + 1)">+</button>
        </div>
        <div>{{ altura }} cm</div>
      </div>

      <div class="input-box peso">
        <label>Peso</label>
        <div class="range-control">
          <button @click="peso = Math.max(30, peso - 1)">−</button>
          <input
            type="range"
            min="30"
            max="150"
            :value="peso"
            @input="(e) => (peso = Number(e.target.value))"
          />
          <button @click="peso = Math.min(150, peso + 1)">+</button>
        </div>
        <div>{{ peso }} kg</div>
      </div>
    </div>

    <div class="resultado">
      <p id="indice">Índice de Masa Corporal (IMC)</p>
      <div class="valor-imc">{{ imc.toFixed(1) }}</div>
      <div class="etiqueta">{{ estadoIMC }}</div>
      <div class="barra-imc">
        <div
          class="indicador"
          :style="{ left: calcularPosicion() + '%' }"
        ></div>
      </div>
      <div class="valores">
        <span>5</span><span>18.5</span><span>25</span><span>30</span
        ><span>40</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.imc-wrapper {
  display: flex;
  flex-direction: row;
  gap: 6%;
  align-items: stretch;
  color: white;
  flex: 1;
  max-width: 100%;
  box-sizing: border-box;
  flex-wrap: nowrap;
}

.inputs {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  gap: 1%;
}

.resultado {
  flex: 0 0 50%;
  background-color: #2d2d2d;
  border-radius: 0 10% 10% 0;
  padding: 6%;
  display: flex;
  flex-direction: column;
  text-align: center;
  box-sizing: border-box;
}

.input-box {
  flex: 1;
  background-color: #ffe5b4;
  padding: 10%;
  border-radius: 10% 0 0 10%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: black;
  box-sizing: border-box;
}

.peso {
  background-color: #caf0f8;
}
.range-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  box-sizing: border-box;
}

.range-control input[type="range"] {
  flex: 1;
  width: 5vw;
}

.range-control button {
  background-color: #7f5af0;
  color: white;
  border: none;
  border-radius: 60%;
  width: 5%;
  height: 40%;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}

.range-control button:hover {
  background-color: #5b3ecb;
}

.resultado {
  background-color: #2d2d2d;
  border-radius: 0 10% 10% 0;
  padding: 6%;
  width: 42%;
  display: flex;
  flex-direction: column;
  text-align: center;
  box-sizing: border-box;
}

.valor-imc {
  font-size: 1.5em;
  font-weight: bold;
}

.etiqueta {
  background-color: #47c758;
  padding: 1%;
  border-radius: 1.2vh;
  display: inline-block;
  font-weight: bold;
  margin-bottom: 10%;
}

.barra-imc {
  height: 1vh;
  background: linear-gradient(to right, #00b4d8, #90e0ef, #ffe066, #ff6b6b);
  border-radius: 5em;
  position: relative;
  width: 100%;
}

.indicador {
  position: absolute;
  top: -0.3vh;
  width: 0.5vw;
  height: 1.5vh;
  background-color: red;
  border-radius: 4vh;
}

.valores {
  display: flex;
  justify-content: space-between;
  font-size: small;
  color: #ccc;
}

#indice {
  font-size: 0.9em;
  margin-top: 12%;
}

@media (max-width: 768px) {
  .imc-wrapper {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    width: 100%;
  }

  .inputs {
    width: 100%;
    height: 100%;
    gap: 2rem;
  }

  .input-box {
    width: 100%;
    border-radius: 15px;
    padding: 1rem;
  }

  .resultado {
    width: 100%;
    border-radius: 8px;
    padding: 1.5rem;
  }

  .valor-imc {
    font-size: 2rem;
  }

  .etiqueta {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  .barra-imc {
    height: 1rem;
    border-radius: 10px;
  }

  .indicador {
    width: 2px;
    height: 1.5rem;
  }

  .valores {
    font-size: 0.9rem;
    margin-top: 0.5rem;
  }
  .range-control button {
    width: 20%;
    height: 50%;
  }
}
@media (min-width: 769px) and (max-width: 1370px) {
  .imc-wrapper {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    width: 100%;
    font-size: 1.5rem;
  }

  .inputs {
    width: 100%;
    height: 100%;
    gap: 2rem;
  }

  .input-box {
    width: 100%;
    border-radius: 15px;
    padding: 1rem;
  }

  .resultado {
    width: 100%;
    border-radius: 8px;
    padding: 1.5rem;
  }

  .valor-imc {
    font-size: 3rem;
  }

  .etiqueta {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .barra-imc {
    height: 1rem;
    border-radius: 10px;
  }

  .indicador {
    width: 2px;
    height: 1.5rem;
  }

  .valores {
    font-size: 1.2rem;
    margin-top: 0.5rem;
  }
  .range-control button {
    width: 6%;
  }
}
</style>
