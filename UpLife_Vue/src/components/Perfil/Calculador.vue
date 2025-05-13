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
    altura(nuevaAltura) {
      this.$emit("updateAltura", nuevaAltura);
    },
    peso(nuevoPeso) {
      this.$emit("updatePeso", nuevoPeso);
    },
  },
  computed: {
    imc() {
      const alturaM = this.altura / 100;
      return this.peso / (alturaM * alturaM);
    },
    estadoIMC() {
      const v = this.imc;
      if (v < 18.5) return "Baixo peso";
      if (v < 25) return "Saudable";
      if (v < 30) return "Sobrepeso";
      return "Obesidade";
    },
  },
  methods: {
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

s
<template>
  <div class="imc-wrapper">
    <div class="inputs">
      <div class="input-box altura">
        <label>Altura</label>
        <input type="range" min="100" max="220" v-model="altura" />
        <div>{{ altura }} cm</div>
      </div>
      <div class="input-box peso">
        <label>Peso</label>
        <input type="range" min="30" max="150" v-model="peso" />
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
#indice {
  font-size: 0.9em;
  margin-top: 12%;
}
.imc-wrapper {
  display: flex;
  gap: 6%;
  align-items: stretch;
  color: white;
  flex: 1;
}

.inputs {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 5%;
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
}

.peso {
  background-color: #caf0f8;
}
.resultado {
  background-color: #2d2d2d;
  border-radius: 0 10% 10% 0;
  padding: 6%;
  width: 40%;
  display: flex;
  flex-direction: column;
  text-align: center;
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
  /* border: 1px solid red; */
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
  font-size: 2vh;
  color: #ccc;
}
</style>
