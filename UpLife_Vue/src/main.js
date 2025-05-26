import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import piniaPersistedState from "pinia-plugin-persistedstate";
import VCalendar from "v-calendar";
import "v-calendar/style.css";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPersistedState);
app.use(pinia); // usar pinia
app.use(router); // usar router
app.use(VCalendar, {
  componentPrefix: "vc", // usar <vc-calendar /> en lugar de <v-calendar />
});
app.mount("#app");
