<template>
  <div class="componet-div">
    <div class="options-div">
      <select v-model="selectedSource" @change="updateOptions" class="bordes">
        <option value="">Seleccione el horigen</option>
        <option value="RaptorDetector">Raptor Detector</option>
        <option value="BirdDetector">Bird Detector</option>
        <option value="Ambos">Ambos</option>
      </select>

      <select v-model="selectedClass" :disabled="!selectedSource" class="bordes">
        <option value="">Selecciona una clase</option>
        <option v-for="option in options2" :value="option.value" :key="option.value">
          {{ option.label }}
        </option>
      </select>
      <button type="submit" class="btn btn-primary" v-on:click="getImages">Filtrar</button>
    </div>
    <div class="flex-container">
      <div v-for="(item) in visibleItems" :key="item.id" class="flex-item" >
        <div @click="mostrarDetalle(item.id)">
          <ImageContainer v-bind:image-src="item.url" v-bind:id="item.id.toString()" v-bind:class-detection="item.class" v-bind:date-detection="item.date" loading="lazy">
          </ImageContainer>
        </div>
        <div v-if="imagenDetalleIndex === item.id" class="imagen-detalle">
          <img :src="item.url" alt="Imagen Detalle" />
          <button @click="cerrarDetalle">Cerrar</button>
        </div>
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
      selectedClass: "",
      options2: [],
      imagenDetalleIndex: null,
    };
  },
  created() {
    this.getImages()
  }
  ,
  methods: {
        async getImages() {
          if(this.selectedClass==="")
          {
            this.selectedClass='All'
          }
          return await fetch("http://127.0.0.1:5000/getsAll", {
            method: 'POST',
            headers: {
              'source': this.selectedSource,
              'class': this.selectedClass
            }
          }).then(response => {
            return response.json()
          }).then(jsonResponse=>
          {
            console.log(jsonResponse)
            this.items=jsonResponse
            this.visibleItems=this.items
            console.log(this.visibleItems)
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
              { value: "All", label: "Todas" },

            ];
            this.selectedClass = "";
          } else if (this.selectedSource === "BirdDetector") {
            this.options2 = [
              { value: "ave_volando", label: "ave volando" },
              { value: "ave_posada", label: "ave posada" },
              { value: "ave_tierra", label: "ave en tierra" },
              { value: "All", label: "Todas" },

            ];
            this.selectedClass = "";
          } else {
            this.options2 = [
              { value: "opcion1_0", label: "seleccione una opcion anteriro" },
            ];
            this.selectedClass = "";
          }
        },
    mostrarDetalle(index) {
      this.imagenDetalleIndex = index;
    },
    cerrarDetalle() {
      this.imagenDetalleIndex = null;
    },

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

.bordes
{
  border:1px solid #2c3e50;
}

.imagen-detalle {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.7);
  padding: 20px;
  text-align: center;
  z-index: 1; /* Para que el detalle esté encima de las otras imágenes */
  max-width: 80%; /* Ajusta el ancho máximo según sea necesario */
  max-height: 80%; /* Ajusta la altura máxima según sea necesario */
  overflow: auto; /* Agrega desplazamiento si la imagen es demasiado grande */
  border-radius: 10px; /* Bordes redondeados */
}

</style>