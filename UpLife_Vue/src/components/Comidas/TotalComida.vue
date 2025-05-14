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
    totalMacros() {
      return this.proteinaTotal + this.graxaTotal + this.carbohidratoTotal || 1;
    },
    proteinaPorcentaxeReal() {
      return (this.proteinaTotal / this.totalMacros) * 100;
    },
    graxaPorcentaxeReal() {
      return (this.graxaTotal / this.totalMacros) * 100;
    },
    carboPorcentaxeReal() {
      return (this.carbohidratoTotal / this.totalMacros) * 100;
    },
    // Solo para mostrar números redondeados en las tarjetas
    proteinaPorcentaxe() {
      return Math.round(this.proteinaPorcentaxeReal);
    },
    graxaPorcentaxe() {
      return Math.round(this.graxaPorcentaxeReal);
    },
    carboPorcentaxe() {
      return Math.round(this.carboPorcentaxeReal);
    },
  },

  mounted() {
    this.cargarDatos();
  },
  methods: {
    async cargarDatos() {
      const usuarioStore = useUsuarioStore();
      const idUsuario = usuarioStore.id;
      try {
        const response = await fetch("http://localhost:8001/api/comidas/");
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

          // Escalado si la suma de macros por 100g supera 100
          const factor = totalMacros100g > 100 ? 100 / totalMacros100g : 1;

          this.pesoTotal += peso;
          this.proteinaTotal += (item.proteinas * peso * factor) / 100;
          this.graxaTotal += (item.graxas * peso * factor) / 100;
          this.carbohidratoTotal += (item.carbohidratos * peso * factor) / 100;

          if (totalMacros100g > 100) {
            console.warn(
              `⚠️ Macros excesivos en '${item.nome}': ${totalMacros100g}g por 100g. Se aplicó corrección.`
            );
          }
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

    <!-- Donut Chart -->
    <div class="donut-chart">
      <svg viewBox="0 0 36 36" class="circular-chart">
        <circle class="bg" cx="18" cy="18" r="15.9155" />
        <!-- Proteínas (verde) - primero para que quede debajo -->
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
        <!-- Grasas (amarillo) -->
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
        <!-- Carbohidratos (azul) - último para que quede encima -->
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
</style>
