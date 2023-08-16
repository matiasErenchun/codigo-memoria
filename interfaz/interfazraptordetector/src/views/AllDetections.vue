
<template>
  <div class="componet-div">
    <div class="options-div">
      <select v-model="selectedSource" @change="updateOptions">
        <option value="">Seleccione el horigen</option>
        <option value="RaptorDetector">Raptor Detector</option>
        <option value="BirdDetector">Bird Detector</option>
        <option value="Ambos">Ambos</option>
      </select>

      <select v-model="selectedOption2" :disabled="!selectedSource">
        <option value="">Selecciona una clase</option>
        <option v-for="option in options2" :value="option.value" :key="option.value">
          {{ option.label }}
        </option>
      </select>
    </div>
    <div class="flex-container">
      <div v-for="(item) in visibleItems" :key="item.id" class="flex-item">
        <ImageContainer :image-src="item.url" :image-name="item.id.toString()" loading="lazy">
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
      selectedSource: "",
      selectedOption2: "",
      options2: [],
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
        },
        updateOptions() {
          if (this.selectedSource === "RaptorDetector" || this.selectedSource === "Ambos") {
            this.options2 = [
              { value: "ave_volando", label: "ave volando" },
              { value: "ave_posada", label: "ave posada" },
              { value: "ave_tierra", label: "ave en tierra" },
              { value: "ave_rapaz_volando", label: "ave rapaz volando" },
              { value: "ave_rapaz_posada", label: "ave rapaz posada" },
              { value: "ave_rapaz_tierra", label: "ave rapaz en tierra" },
              { value: "Todas", label: "Todas" },

            ];
            this.selectedOption2 = "";
          } else if (this.selectedSource === "BirdDetector") {
            this.options2 = [
              { value: "ave_volando", label: "ave volando" },
              { value: "ave_posada", label: "ave posada" },
              { value: "ave_tierra", label: "ave en tierra" },
              { value: "Todas", label: "Todas" },

            ];
            this.selectedOption2 = "";
          } else {
            this.options2 = [
              { value: "opcion1_0", label: "seleccione una opcion anteriro" },
            ];
            this.selectedOption2 = "";
          }
        }
  }
}


</script>

<style scoped>
.flex-container {
  display: flex;
  flex-wrap: wrap; /* Esto permite que los elementos se envuelvan en una nueva fila */
  justify-content: center;
}
.flex-item {
  flex: 1; /* Esto hace que los elementos ocupen el mismo espacio disponible */
  margin: 10px; /* Agrega margen para separar los elementos */
  max-width: 30%;
  max-height: 35%;
}
.componet-div
{
  margin-left: 5%;
  margin-right: 5%;
  justify-content: center;
}

.options-div
{
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

</style>