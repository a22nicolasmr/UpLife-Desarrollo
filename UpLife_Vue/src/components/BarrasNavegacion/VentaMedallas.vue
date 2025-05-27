<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>
<template>
  <div class="modal-mask">
    <transition name="fade">
      <div class="modal-container">
        <h1>Nova medalla obtida</h1>
      </div>
    </transition>
  </div>
</template>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

a {
  display: flex;
  justify-self: right;
  cursor: pointer;
  font-weight: 600;
}
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: right;
}
.modal-container {
  width: 18%;
  height: 10%;
  margin-right: 2%;
  margin-top: 2%;
  padding: 20px 30px;
  background-color: white;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  border-radius: 8px;
}
@media (max-width: 768px) {
  .modal-container {
    width: 87%;
    height: 9%;
    padding: 15px 20px;
    border-radius: 10px;
  }

  .modal-container h1 {
    font-size: xx-large;
    text-align: center;
  }
}
@media (max-width: 1370px) {
  .modal-container {
    width: 87%;
    height: 9%;
    padding: 15px 20px;
    border-radius: 10px;
  }

  .modal-container h1 {
    font-size: xx-large;
    text-align: center;
  }
}
</style>
