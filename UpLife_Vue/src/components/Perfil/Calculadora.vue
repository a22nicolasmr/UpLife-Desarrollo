<script>
import Calculador from "./Calculador.vue";
import { useUsuarioStore } from "@/stores/useUsuario";

export default {
  components: {
    Calculador,
  },
  data() {
    return {
      selectedObxectivo: "",
      selectedActividade: "",
      selectedXenero: "",
      idade: 0,
      alturaSeleccionada: null,
      pesoSeleccionado: null,
      xenero: "",
    };
  },
  computed: {
    id() {
      const store = useUsuarioStore();
      return store.id;
    },
  },

  methods: {
    // coller altura e peso do compoñente Calculador
    actualizarAltura(valor) {
      this.alturaSeleccionada = valor;
      console.log("Altura desde hijo:", valor);
    },
    actualizarPeso(valor) {
      this.pesoSeleccionado = valor;
      console.log("Peso desde hijo:", valor);
    },

    // actualizar valores do usuario cos valores metidos cando se pulsa boton Calcular
    async actualizarApi() {
      // Paso 1: calcular TMB (gasto basal)
      const {
        pesoSeleccionado: peso,
        alturaSeleccionada: altura,
        idade,
        selectedXenero: xenero,
        selectedActividade: actividade,
        selectedObxectivo: obxectivo,
      } = this;

      let tmb = 0;
      if (xenero === "Home") {
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5;
      } else {
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161;
      }

      // Paso 2: factor de actividade
      const factoresActividad = {
        Sedentario: 1.2,
        "Pouco activo": 1.375,
        Normal: 1.55,
        Activo: 1.725,
        "Moi activo": 1.9,
      };
      const factorActividad = factoresActividad[actividade] || 1.55;

      // Paso 3: ajustar por obxectivo
      const ajustesObjetivo = {
        "Perder graxa agresivamente": 0.75,
        "Perder graxa lentamente": 0.9,
        "Manter o peso": 1.0,
        "Ganar masa lentamente": 1.1,
        "Ganar masa agresivamente": 1.2,
      };
      const ajusteObjetivo = ajustesObjetivo[obxectivo] || 1;

      const calorias_diarias = Math.round(
        tmb * factorActividad * ajusteObjetivo
      );

      // Paso 4: calcular a auga diaria (35 ml por kg)
      const auga_diaria = Math.round(peso * 35);

      // Paso 5: Enviar PATCH
      const datos = {
        xenero,
        altura,
        peso,
        obxectivo,
        actividade,
        idade,
        calorias_diarias,
        auga_diaria,
      };

      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/usuarios/${this.id}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(datos),
          }
        );

        const resultado = await response.json();
        console.log("Usuario actualizado con medidas:", resultado);
        this.$emit("actualizarDatos");
      } catch (error) {
        console.error("Erro ao facer PATCH cos datos:", error);
      }
    },
  },
};
</script>
<template>
  <div id="principal">
    <h3>Calculadora IMC</h3>
    <Calculador
      @updateAltura="actualizarAltura"
      @updatePeso="actualizarPeso"
    ></Calculador
    ><br />
    <h3>Calculadora de Auga e Calorias</h3>
    <form action="">
      <label for="inputXenero">Xénero</label>
      <select name="inputXenero" id="inputXenero" v-model="selectedXenero">
        <option value="">Seleccionar</option>

        <option value="Home">Home</option>
        <option value="Muller">Muller</option>
      </select>
      <label for="inputObxectivo">Obxectivo</label>
      <select
        name="inputObxectivo"
        id="inputObxectivo"
        v-model="selectedObxectivo"
      >
        <option value="">Seleccionar</option>
        <option value="Perder graxa agresivamente">
          Perder graxa agresivamente
        </option>
        <option value="Perder graxa lentamente">Perder graxa levemente</option>
        <option value="Manter o peso">Manter o peso</option>
        <option value="Ganar masa lentamente">Gañar masa levemente</option>
        <option value="Ganar masa agresivamente">
          Gañar masa agresivamente
        </option>
      </select>
      <label for="inputActividade">Actividade</label>
      <select
        name="inputActividade"
        id="inputActividade"
        v-model="selectedActividade"
      >
        <option value="">Seleccionar</option>
        <option value="Moi activo">Moi activo</option>
        <option value="Activo">Activo</option>
        <option value="Normal">Normal</option>
        <option value="Pouco activo">Pouco activo</option>
        <option value="Sedentario">Sedentario</option>
      </select>
      <label for="inputIdade">Idade</label>
      <input
        type="number"
        id="inputIdade"
        placeholder="Ingresa a tua idade"
        v-model.number="idade"
      />
      <button type="submit" @click.prevent="actualizarApi()">Calcular</button>
    </form>
  </div>
</template>
<style scoped>
h1 {
  color: white;
}
.calculadora {
  max-width: 100%;
  width: 100%;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.calculadora form {
  width: 100%;
  align-items: start;
}

#principal {
  height: 100%;
  overflow-y: auto;
  padding: 1rem;
  box-sizing: border-box;
}

.calculadora select,
.calculadora input {
  width: 100%;
  padding: 2.5%;
  margin-bottom: 1%;
  background-color: #eff0f2;
  border: none;
  border-radius: 2px;
  font-size: 0.8em;
  color: #043133;
  box-sizing: border-box;
}

.calculadora select::placeholder,
.calculadora input::placeholder {
  color: #838383;
}

.calculadora button {
  width: 100%;
  padding: 3%;
  background-color: #4880ff;
  color: white;
  border: none;
  border-radius: 2px;
  font-size: medium;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 2%;
}

.calculadora button:hover {
  background-color: #007074;
}

.calculadora p {
  text-align: left;
  color: white;
}
</style>
