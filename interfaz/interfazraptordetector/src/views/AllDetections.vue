
<template>
  <div>
    <div>
      <p>filtros</p>
    </div>
    <div>
      <div v-for="(item) in visibleItems" :key="item.id">
        <ImageContainer :image-src="item.url" :image-name="item.id" loading="lazy">
        </ImageContainer>
      </div>
    </div>
  </div>

</template>
<script>

import ImageContainer from "@/components/ImageContainer.vue";

export default {
  components: {ImageContainer},
  data() {
    return {
      items: [],
      visibleItems: [],
      pageSize: 10,
      currentPage: 1,
      loading: false,
      selectedSource:" "
    };
  },
  created() {
    this.getImages()
  }
  ,
  methods: {
        async getImages() {
          return await fetch("http://127.0.0.1:5000/getsAll", {
            method: 'POST',
            headers: {
              'source': this.selectedSource
            }
          }).then(response => {
            return response.json()
          }).then(jsonResponse=>
          {
            console.log(jsonResponse)
            this.items=jsonResponse
            this.visibleItems=this.items
          }).catch(() => {
            this.alertConfig.show = true;
            this.alertConfig.type = "error";
            this.alertConfig.message = "Ocurrio un error al cargar la imagen"
            this.isLoading = false

          })
        }
      }
}


</script>

<style scoped>

</style>