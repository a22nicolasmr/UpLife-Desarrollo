import { defineStore } from "pinia";

export const useUsuarioStore = defineStore("usuario", {
  state: () => ({
    id: null,
    nome: "",
    imagen: "image/upload/v1747728142/usuario_xotela.png",
    medallas: 0,
    altura: 0,
    peso: 0,
    xenero: "",
    obxectivo: "",
    actividade: "",
    idade: 0,
    calorias: 0,
    auga: 0,
    token: localStorage.getItem("token"),
  }),
  actions: {
    cargarToken() {
      this.token = localStorage.getItem("token");
    },
    guardarToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
    },
    limpiarToken() {
      this.token = null;
      localStorage.removeItem("token");
    },
    // cargar todos os datos de usuario
    async cargarUsuario(nome) {
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

        const ruta = usuario.imaxe_perfil;
        this.imagen = ruta || "image/upload/v1747728142/usuario_xotela.png";

        //gardar solo o necesario en localStorage
        localStorage.setItem(
          "usuario",
          JSON.stringify({
            id: this.id,
            nome: this.nome,
          })
        );

        //cargar medallas de usuario
        await this.cargarMedallas();
      } catch (error) {
        console.error("Error cargando datos del usuario:", error);
      }
    },

    //cargar medallas de usuario
    async cargarMedallas() {
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
        console.error("Error cargando medallas:", error);
      }
    },

    //cargar datos de usuario desde localStorage
    cargarDesdeStorage() {
      const datos = localStorage.getItem("usuario");
      if (datos) {
        const { id, nome } = JSON.parse(datos);
        this.id = id;
        this.nome = nome;
        this.cargarMedallas();
      }
    },

    //gardar datos actualizados do usuario
    guardarUsuarioActualizado() {
      localStorage.setItem(
        "usuario",
        JSON.stringify({
          id: this.id,
          nome: this.nome,
          imagen: this.imagen,
          altura: this.altura,
          peso: this.peso,
          xenero: this.xenero,
          obxectivo: this.obxectivo,
          actividade: this.actividade,
          idade: this.idade,
          calorias: this.calorias,
          auga: this.auga,
        })
      );
    },

    //eliminar datos do usuario cando se pecha a sesion
    cerrarSesion() {
      localStorage.removeItem("usuario");
      this.id = null;
      this.nome = "";
      this.imagen = "/imaxes/usuario.png";
      this.medallas = 0;
    },

    //actualizar datos usuario
    async actualizarDatos() {
      if (this.id) {
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
          this.actividade = data.actividade;
          this.idade = data.idade;
          this.calorias = data.calorias_diarias;
          this.auga = data.auga_diaria;

          this.guardarUsuarioActualizado();
        } catch (error) {
          console.error("Erro ao actualizar datos:", error);
        }
      }
    },

    //actualizar numero de medallas filtradas por se están ou non completadas
    async updateNumeroMedallas() {
      fetch("https://uplife-final.onrender.com/api/medallas/", {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          const completadas = data.filter(
            (m) => m.usuarios.includes(this.id) && m.completado
          );
          this.medallas = completadas.length;
        })
        .catch((err) => console.error("Erro cargando medallas:", err));
    },
  },
  //cargar datos desde localStorage se existen
  persist: true,
});
