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
      mensaxeErro: "",
    };
  },
  computed: {
    // obter o id do usuario do store
    id() {
      const store = useUsuarioStore();
      return store.id;
    },

    // obter o token de autenticación
    token() {
      return useUsuarioStore().token;
    },
  },

  methods: {
    // validar os campos do formulario
    validarFormulario() {
      const erros = [];

      if (!this.selectedXenero) erros.push("Selecciona un xénero.");
      if (!this.selectedObxectivo) erros.push("Selecciona un obxectivo.");
      if (!this.selectedActividade)
        erros.push("Selecciona un nivel de actividade.");
      if (!this.idade || this.idade <= 0)
        erros.push("Introduce unha idade válida.");
      if (!this.alturaSeleccionada || this.alturaSeleccionada <= 0)
        erros.push("Introduce unha altura válida.");
      if (!this.pesoSeleccionado || this.pesoSeleccionado <= 0)
        erros.push("Introduce un peso válido.");

      if (erros.length > 0) {
        this.mensaxeErro = erros[0]; // mostrar só o primeiro erro
        return false;
      }

      this.mensaxeErro = ""; // limpar erros se todo está ben
      return true;
    },

    // actualizar altura desde Calculador
    actualizarAltura(valor) {
      this.alturaSeleccionada = valor;
    },

    // actualizar peso desde Calculador
    actualizarPeso(valor) {
      this.pesoSeleccionado = valor;
    },

    // actualizar datos do usuario na API
    async actualizarApi() {
      if (!this.validarFormulario()) return;

      const {
        pesoSeleccionado: peso,
        alturaSeleccionada: altura,
        idade,
        selectedXenero: xenero,
        selectedActividade: actividade,
        selectedObxectivo: obxectivo,
      } = this;

      // calcular gasto basal
      let tmb = 0;
      if (xenero === "Home") {
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5;
      } else {
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161;
      }

      // aplicar factor de actividade
      const factoresActividad = {
        Sedentario: 1.2,
        "Pouco activo": 1.375,
        Normal: 1.55,
        Activo: 1.725,
        "Moi activo": 1.9,
      };
      const factorActividad = factoresActividad[actividade] || 1.55;

      // aplicar axuste segundo obxectivo
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

      // calcular auga diaria (35 ml por kg)
      const auga_diaria = Math.round(peso * 35);

      // preparar datos para actualizar
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
              Authorization: `Bearer ${this.token}`,
            },
            body: JSON.stringify(datos),
          }
        );

        const resultado = await response.json();

        // emitir evento para actualizar datos no compoñente pai
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
      <span v-if="mensaxeErro" class="error">{{ mensaxeErro }}</span>
    </form>
  </div>
</template>
<style scoped>
.error {
  color: #ff4d4d;
  display: block;
  margin-top: 2%;
  font-size: medium;
}
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

@media (max-width: 1370px) {
  h3 {
    font-size: 2rem;
  }
  form {
    font-size: 1.75rem;
  }
}
</style>
