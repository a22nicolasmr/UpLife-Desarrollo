import { createRouter, createWebHistory } from "vue-router";

import Formularios from "@/views/Formularios.vue";
import Inicio from "@/components/Formularios/Inicio.vue";
import Rexistro from "@/components/Formularios/Rexistro.vue";
import Tarefas from "@/views/Tarefas.vue";
import ListaTarefas from "@/components/Tarefas/ListaTarefas.vue";
import EngadirTarefas from "@/components/Tarefas/EngadirTarefas.vue";
import Auga from "@/views/Auga.vue";
import Comidas from "@/views/Comidas.vue";
import Exercicios from "@/views/Exercicios.vue";
import Medallas from "@/views/Medallas.vue";
import Perfil from "@/views/Perfil.vue";
import Plantillas from "@/views/Plantillas.vue";
import Calculadora from "@/components/Perfil/Calculadora.vue";
import Calculador from "@/components/Perfil/Calculador.vue";
import EngadirAuga from "@/components/Auga/EngadirAuga.vue";
import HistorialAuga from "@/components/Auga/HistorialAuga.vue";
import EngadirComida from "@/components/Comidas/EngadirComida.vue";
import GrupoComida from "@/components/Comidas/GrupoComida.vue";
import HistorialComidas from "@/components/Comidas/HistorialComidas.vue";
import TotalComida from "@/components/Comidas/TotalComida.vue";
import EngadirExercicios from "@/components/Exercicios/EngadirExercicios.vue";
import EngadirExercicioPlantilla from "@/components/Plantillas/EngadirExercicioPlantilla.vue";
import EngadirPlantillasExercicios from "@/components/Exercicios/EngadirPlantillasExercicios.vue";
import HistorialExercicios from "@/components/Exercicios/HistorialExercicios.vue";
import NovaPlantilla from "@/components/Plantillas/NovaPlantilla.vue";
import Condicions from "@/views/Condicions.vue";
import Cambio from "@/components/Formularios/Cambio.vue";

const routes = [
  {
    // redirixir a tarefas cando se abre a aplicacion
    path: "/",
    // redirect: "/tarefas",
    redirect: "/formularios/rexistro",
  },
  {
    path: "/formularios",
    name: "formularios",
    component: Formularios,
    redirect: "/formularios/rexistro",
    children: [
      {
        path: "inicio",
        name: "inicio",
        component: Inicio,
      },
      {
        path: "rexistro",
        name: "rexistro",
        component: Rexistro,
      },
      {
        path: "cambio",
        name: "cambio",
        component: Cambio,
      },
    ],
  },
  {
    path: "/tarefas",
    name: "tarefas",
    component: Tarefas,
    children: [
      {
        path: "listaTarefas",
        name: "listaTarefas",
        component: ListaTarefas,
      },
      {
        path: "engadirTarefas",
        name: "engadirTarefas",
        component: EngadirTarefas,
      },
    ],
  },
  {
    path: "/auga",
    name: "auga",
    component: Auga,
    children: [
      {
        path: "engadirAuga",
        name: "engadirAuga",
        component: EngadirAuga,
      },
      {
        path: "historialAuga",
        name: "historialAuga",
        component: HistorialAuga,
      },
    ],
  },
  {
    path: "/comidas",
    name: "comidas",
    component: Comidas,
    children: [
      {
        path: "engadirComida",
        name: "engadirComida",
        component: EngadirComida,
      },
      {
        path: "grupoComida",
        name: "grupoComida",
        component: GrupoComida,
      },
      {
        path: "historialComidas",
        name: "historialComidas",
        component: HistorialComidas,
      },
      {
        path: "totalComida",
        name: "totalComida",
        component: TotalComida,
      },
    ],
  },
  {
    path: "/exercicios",
    name: "exercicios",
    component: Exercicios,
    children: [
      {
        path: "engadirExercicios",
        name: "engadirExercicios",
        component: EngadirExercicios,
      },
      {
        path: "engadirPlantillasExercicios",
        name: "engadirPlantillasExercicios",
        component: EngadirPlantillasExercicios,
      },
      {
        path: "historialExercicios",
        name: "historialExercicios",
        component: HistorialExercicios,
      },
    ],
  },
  {
    path: "/medallas",
    name: "medallas",
    component: Medallas,
  },
  {
    path: "/perfil",
    name: "perfil",
    component: Perfil,
    children: [
      {
        path: "calculadora",
        name: "calculadora",
        component: Calculadora,
        children: [
          {
            path: "calculador",
            name: "calculador",
            component: Calculador,
          },
        ],
      },
    ],
  },
  {
    path: "/plantillas",
    name: "plantillas",
    component: Plantillas,
    children: [
      {
        path: "engadirExercicioPlantilla",
        name: "engadirExercicioPlantilla",
        component: EngadirExercicioPlantilla,
      },
      {
        path: "novaPlantilla",
        name: "novaPlantilla",
        component: NovaPlantilla,
      },
    ],
  },
  {
    path: "/condicions",
    name: "condicions",
    component: Condicions,
  },
];

// creacion do router coas rutas
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
