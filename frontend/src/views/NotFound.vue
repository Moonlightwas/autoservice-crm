<template>
  <div class="not-found">
    <div class="bg-image"></div>
    <div class="overlay"></div>
    <div class="content">
      <h1>404</h1>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  overflow: hidden;
}
.bg-image {
  position: absolute;
  inset: 0;
  background-image: url("https://i.pinimg.com/736x/ce/02/bb/ce02bb9a941917096b522174b7214667.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  transform-origin: center center;
  transform: scaleX(1.3) translateX(-10px);
}
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1;
}
.content {
  position: relative;
  z-index: 2;
  text-align: center;
}
h1 {
  font-size: 180px;
  color: #ff3e3e;
  -webkit-text-stroke: 2px #3a0f0f;
  letter-spacing: 10px;
  font-family: 'Arial Black', sans-serif;
}

@media (max-width: 768px) {
  h1 {
    font-size: 150px;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 120px;
    letter-spacing: 5px;
  }
}
</style>