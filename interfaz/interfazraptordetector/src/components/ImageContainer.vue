
<template>
  <div class="ImageContainer">
    <img :src="imageSrc">
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
  min-width: 100px;
  min-height: 50px;
  background-color: #2c3e50;
}
</style>