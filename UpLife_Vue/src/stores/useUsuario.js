import { defineStore } from "pinia";

export const useUsuarioStore = defineStore("usuario", {
  state: () => ({
    id: null,
    nome: "",
    //imaxe por defecto se o usuario non ten imaxe de perfil
    imagen: "image/upload/v1747728142/usuario_xotela.png",
    medallas: 0,
    altura: 0,
    peso: 0,
    email: "",
    xenero: "",
    obxectivo: "",
    actividade: "",
    idade: 0,
    calorias: 0,
    auga: 0,
    modo_aplicacion: "C",
    token: localStorage.getItem("token") || null, // cargar token dende localStorage ao iniciar
  }),

  actions: {
    // cargar o token dende localStorage
    cargarToken() {
      this.token = localStorage.getItem("token");
    },

    // gardar o token no estado e no localStorage
    guardarToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
    },

    // limpar o token do estado e do localStorage
    limpiarToken() {
      this.token = null;
      localStorage.removeItem("token");
    },

    // cargar todos os datos do usuario a partir do nome de usuario
    async cargarUsuario(nome) {
      if (!this.token) return;

      try {
        const response = await fetch(
          "https://uplife-final.onrender.com/api/usuarios/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const usuarios = await response.json();
        const usuario = usuarios.find((u) => u.nome_usuario === nome);
        if (!usuario) return;

        this.id = usuario.id_usuario;
        this.nome = usuario.nome;
        this.email = usuario.email;
        this.imagen =
          usuario.imaxe_perfil || "image/upload/v1747728142/usuario_xotela.png";

        // gardar datos básicos no localStorage
        localStorage.setItem(
          "usuario",
          JSON.stringify({
            id: this.id,
            nome: this.nome,
            email: this.email,
          })
        );

        // cargar medallas do usuario
        await this.cargarMedallas();
      } catch (error) {
        console.error("erro cargando datos do usuario:", error);
      }
    },

    // cargar medallas completadas do usuario
    async cargarMedallas() {
      if (!this.token || !this.id) return;

      try {
        const medallasRes = await fetch(
          "https://uplife-final.onrender.com/api/medallas/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const medallas = await medallasRes.json();
        this.medallas = medallas.filter(
          (m) => m.usuarios.includes(this.id) && m.completado
        ).length;
      } catch (error) {
        console.error("erro cargando medallas:", error);
      }
    },

    // cargar datos do usuario dende o localStorage se existen
    cargarDesdeStorage() {
      const datos = localStorage.getItem("usuario");
      if (datos) {
        const { id, nome, email } = JSON.parse(datos);
        this.id = id;
        this.nome = nome;
        this.email = email || "";
        this.cargarMedallas();
      }
    },

    // gardar datos actualizados do usuario no localStorage
    guardarUsuarioActualizado() {
      localStorage.setItem(
        "usuario",
        JSON.stringify({
          id: this.id,
          nome: this.nome,
          imagen: this.imagen,
          altura: this.altura,
          peso: this.peso,
          email: this.email,
          xenero: this.xenero,
          obxectivo: this.obxectivo,
          actividade: this.actividade,
          idade: this.idade,
          calorias: this.calorias,
          auga: this.auga,
          modo_aplicacion: this.modo_aplicacion,
        })
      );
    },

    // eliminar todos os datos do usuario cando se pecha a sesión
    cerrarSesion() {
      localStorage.removeItem("usuario");
      localStorage.removeItem("token");
      this.token = null;
      this.id = null;
      this.nome = "";
      this.imagen = "image/upload/v1747728142/usuario_xotela.png";
      this.medallas = 0;
      this.altura = 0;
      this.peso = 0;
      this.email = "";
      this.xenero = "";
      this.obxectivo = "";
      this.actividade = "";
      this.idade = 0;
      this.calorias = 0;
      this.auga = 0;
      this.modo_aplicacion = "C";
    },

    // actualizar os datos do usuario coa API
    async actualizarDatos() {
      if (!this.id || !this.token) return;

      try {
        const response = await fetch(
          `https://uplife-final.onrender.com/api/usuarios/${this.id}/`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const data = await response.json();

        this.imagen =
          data.imaxe_perfil || "image/upload/v1747728142/usuario_xotela.png";
        this.nome = data.nome;
        this.altura = data.altura;
        this.peso = data.peso;
        this.xenero = data.xenero;
        this.obxectivo = data.obxectivo;
        this.email = data.email;
        this.actividade = data.actividade;
        this.idade = data.idade;
        this.calorias = data.calorias_diarias;
        this.auga = data.auga_diaria;
        this.modo_aplicacion = data.modo_aplicacion;

        this.guardarUsuarioActualizado();
      } catch (error) {
        console.error("erro ao actualizar datos:", error);
      }
    },

    // actualizar o número de medallas completadas
    async updateNumeroMedallas() {
      if (!this.token || !this.id) return;

      try {
        const res = await fetch(
          "https://uplife-final.onrender.com/api/medallas/",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        const data = await res.json();
        const completadas = data.filter(
          (m) => m.usuarios.includes(this.id) && m.completado
        );
        this.medallas = completadas.length;
      } catch (err) {
        console.error("erro cargando medallas:", err);
      }
    },
  },

  // activar persistencia do estado no localStorage
  persist: true,
});
