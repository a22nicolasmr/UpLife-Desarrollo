<script>
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  data() {
    return {
      comidas: [],
      pesoTotal: 0,
      proteinaTotal: 0,
      graxaTotal: 0,
      carbohidratoTotal: 0,
    };
  },

  computed: {
    // calcular a suma total dos macros
    totalMacros() {
      return this.proteinaTotal + this.graxaTotal + this.carbohidratoTotal || 1;
    },
    // calcular porcentaxe real de proteínas
    proteinaPorcentaxeReal() {
      return (this.proteinaTotal / this.totalMacros) * 100;
    },
    // calcular porcentaxe real de graxas
    graxaPorcentaxeReal() {
      return (this.graxaTotal / this.totalMacros) * 100;
    },
    // calcular porcentaxe real de carbohidratos
    carboPorcentaxeReal() {
      return (this.carbohidratoTotal / this.totalMacros) * 100;
    },

    // redondear porcentaxes
    proteinaPorcentaxe() {
      return Math.round(this.proteinaPorcentaxeReal);
    },
    graxaPorcentaxe() {
      return Math.round(this.graxaPorcentaxeReal);
    },
    carboPorcentaxe() {
      return Math.round(this.carboPorcentaxeReal);
    },

    // obter token do store
    token() {
      return useUsuarioStore().token;
    },
  },

  mounted() {
    // cargar datos ao montar o compoñente
    this.cargarDatos();
  },
  methods: {
    // cargar comidas filtradas por usuario e data actual
    async cargarDatos() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/comidas/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        if (!response.ok) throw new Error("Erro ao cargar comidas");
        const comidas = await response.json();
        const hoxe = new Date().toISOString().split("T")[0];

        const comidasUsuario = comidas.filter(
          (g) => g.usuario === idUsuario && g.data === hoxe
        );
        this.comidas = comidasUsuario;

        this.pesoTotal = 0;
        this.proteinaTotal = 0;
        this.graxaTotal = 0;
        this.carbohidratoTotal = 0;

        this.comidas.forEach((item) => {
          const peso = item.peso;
          const totalMacros100g =
            item.proteinas + item.graxas + item.carbohidratos;

          // calcular cantidades axustadas
          const factor = totalMacros100g > 100 ? 100 / totalMacros100g : 1;

          this.pesoTotal += peso;
          this.proteinaTotal += (item.proteinas * peso * factor) / 100;
          this.graxaTotal += (item.graxas * peso * factor) / 100;
          this.carbohidratoTotal += (item.carbohidratos * peso * factor) / 100;
        });
      } catch (error) {
        console.error("Erro cargando datos:", error);
      }
    },
  },
};
</script>

<template>
  <div class="total-container">
    <div class="cards">
      <div class="card carbs">
        <p>Carbs Totais</p>
        <h3>{{ carbohidratoTotal.toFixed(2) }}g</h3>
        <span>{{ carboPorcentaxe }}%</span>
      </div>
      <div class="card graxas">
        <p>Graxas totais</p>
        <h3>{{ graxaTotal.toFixed(2) }}g</h3>
        <span>{{ graxaPorcentaxe }}%</span>
      </div>
      <div class="card proteinas">
        <p>Proteínas Totais</p>
        <h3>{{ proteinaTotal.toFixed(2) }}g</h3>
        <span>{{ proteinaPorcentaxe }}%</span>
      </div>
      <div class="card peso">
        <p>Peso Total</p>
        <h3>{{ pesoTotal }}g</h3>
      </div>
    </div>

    <div class="donut-chart">
      <svg viewBox="0 0 36 36" class="circular-chart">
        <circle class="bg" cx="18" cy="18" r="15.9155" />
        <!-- proteínas (verde) -->
        <circle
          class="proteinas"
          cx="18"
          cy="18"
          r="15.9155"
          :stroke-dasharray="`${proteinaPorcentaxeReal} ${
            100 - proteinaPorcentaxeReal
          }`"
          stroke-dashoffset="25"
        />
        <!-- graxas (amarelo) -->
        <circle
          class="graxas"
          cx="18"
          cy="18"
          r="15.9155"
          :stroke-dasharray="`${graxaPorcentaxeReal} ${
            100 - graxaPorcentaxeReal
          }`"
          :stroke-dashoffset="25 - proteinaPorcentaxeReal"
        />
        <!-- carbohidratos (azul) -->
        <circle
          class="carbs"
          cx="18"
          cy="18"
          r="15.9155"
          :stroke-dasharray="`${carboPorcentaxeReal} ${
            100 - carboPorcentaxeReal
          }`"
          :stroke-dashoffset="
            25 - (proteinaPorcentaxeReal + graxaPorcentaxeReal)
          "
        />
      </svg>
    </div>
  </div>
</template>

<style scoped>
.total-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
  box-sizing: border-box;
  margin-top: 10%;
  height: "50%";
}

.cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  width: 90%;
  margin-bottom: 2rem;
}

.card {
  background-color: white;
  color: black;
  padding: 1rem;
  border-radius: 12px;
  position: relative;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.card span {
  position: absolute;
  top: 20%;
  right: 15px;
  font-weight: bold;
  background-color: #eee;
  padding: 0.2rem 0.5rem;
  border-radius: 50px;
}
.card.carbs span {
  background-color: #b4b5ff;
  color: #333;
}
.card.graxas span {
  background-color: #ffe6a7;
  color: #333;
}
.card.proteinas span {
  background-color: #a7f3d0;
  color: #333;
}

.donut-chart {
  max-width: 35%;
}
.circular-chart {
  width: 100%;
  height: auto;
  transform: rotate(-90deg);
}
.bg {
  fill: none;
  stroke: #ddd;
  stroke-width: 3.8;
}
.carbs {
  fill: none;
  stroke: #6366f1;
  stroke-width: 3.8;
}
.graxas {
  fill: none;
  stroke: #facc15;
  stroke-width: 3.8;
}
.proteinas {
  fill: none;
  stroke: #10b981;
  stroke-width: 3.8;
}
@media (max-width: 768px) {
  .total-container {
    margin-top: 1rem;
    padding: 1rem;
    height: auto;
    overflow: visible;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  span {
    width: 40%;
  }
  .cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    width: 100%;
    max-width: 500px;
    margin-bottom: 2rem;
  }

  .card {
    font-size: 0.95rem;
    padding: 1rem;
    min-height: 100px;
    text-align: center;
    font-size: small;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-radius: 12px;
  }
  .card p {
    margin: 0;
    margin-bottom: 40%;
  }
  .card span {
    margin-top: 1.5rem;
    font-size: medium;
    font-weight: bold;
    background-color: #eee;
    padding: 0.3rem 0.7rem;
    border-radius: 1rem;
    display: inline-block;
    margin-right: 14%;
  }

  .donut-chart {
    max-width: 80%;
    width: 100%;
    margin: 0 auto;
  }

  .circular-chart {
    width: 100%;
    height: auto;
  }
}
@media (min-width: 769px) and (max-width: 1370px) {
  .total-container {
    margin-top: 1rem;
    padding: 1rem;
    height: auto;
    overflow: visible;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  span {
    width: 40%;
  }
  .cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    width: 100%;
    max-width: 500px;
    margin-bottom: 2rem;
  }

  .card {
    font-size: 0.95rem;
    padding: 1rem;
    min-height: 100px;
    text-align: center;
    font-size: small;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-radius: 12px;
  }
  .card p {
    margin: 0;
    margin-bottom: 40%;
  }
  .card span {
    margin-top: 1.5rem;
    font-size: medium;
    font-weight: bold;
    background-color: #eee;
    padding: 0.3rem 0.7rem;
    border-radius: 1rem;
    display: inline-block;
    margin-right: 14%;
  }

  .donut-chart {
    max-width: 80%;
    width: 100%;
    margin: 0 auto;
  }

  .circular-chart {
    width: 100%;
    height: auto;
  }
}
</style>
