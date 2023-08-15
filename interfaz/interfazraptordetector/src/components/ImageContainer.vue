
<template>
  <div class="ImageContainer">
    <img :src="imageSrc" class="responsive-image">
    <p>{{imageName}}</p>
  </div>
</template>

<script>
export default {
  props: {
    imageSrc: String,
    imageName: String
  },
};
</script>

<style scoped>
.ImageContainer
{
  min-width: 150px;
  min-height: 50px;
  max-height: 100%;
  max-width: 100%;
  justify-content: center; /* Centrar contenido horizontalmente */
  align-items: center;
  background-color: #2c3e50;
}
.responsive-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* Ajustar la imagen manteniendo su relación de aspecto */
}
</style>