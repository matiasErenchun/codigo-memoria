<template>
  <div class="componet-div">
    <!-------------!filter section!--->
    <div class="options-div input-container">
      <div v-if="masFiltros!==true">
        <button type="button" class="btn btn-dark" @click="this.changeMoreFilters">+</button>
      </div>
      <div v-else>
        <button type="button" class="btn btn-dark" @click="this.changeMoreFilters">-</button>
      </div>
      <select v-model="selectedSource" @change="updateOptions" class="input">
        <option value="">Seleccione el horigen</option>
        <option value="RaptorDetector">Raptor Detector</option>
        <option value="BirdDetector">Bird Detector</option>
        <option value="Ambos">Ambos</option>
      </select>

      <select v-model="selectedClass" :disabled="!selectedSource" class="input">
        <option value="">Selecciona una clase</option>
        <option v-for="option in options2" :value="option.value" :key="option.value">
          {{ option.label }}
        </option>
      </select>
      <button type="submit" class="btn btn-primary" v-on:click="getImages">Filtrar</button>
    </div>
    <div v-if="masFiltros===true" class="filtros">
      <div class="options-div">
        <div class="input-container">
          <label for="fechaInicio" :class="{ 'label-up': fechaInicio }">Fecha de Inicio:</label>
          <input type="datetime-local" id="fechaInicio" v-model="fechaInicio" />
        </div>
        <div class="input-container">
          <label for="fechaFin" :class="{ 'label-up': fechaFin }">Fecha de Fin:</label>
          <input type="datetime-local" id="fechaFin" v-model="fechaFin" />
        </div>
      </div>
    </div>
    <!--------! image section!------>
    <div class="flex-container">
      <div v-for="(item) in visibleItems" :key="item.id" class="flex-item" >
        <div @click="mostrarDetalle(item.id)">
          <ImageContainer v-bind:image-src="item.url" v-bind:id="item.id.toString()" v-bind:class-detection="item.class" v-bind:date-detection="item.date" loading="lazy">
          </ImageContainer>
        </div>
        <div v-if="imagenDetalleIndex === item.id" class="imagen-detalle">
          <div>
            <img :src="item.url" alt="Imagen Detalle" class="responsive-image"/>
          </div>
          <div class="contenedor-texto">
            <div class="fila">
              <p class="letra-pequena margen-derecho">Id: {{item.id}}</p>
              <p class="letra-pequena"> Clase: {{ formatearClase(item.class)}}</p>
            </div>
            <button @click="cerrarDetalle">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
    <!----- pagination controll!----->
    <div>
      <button @click="previousPage" class="btn btn-light"> Anterior </button>
      <button :disabled=false class="boton-bonito">{{paginaActual +1}}</button>
      <button @click="nextPage" class="btn btn-light">Siguente</button>
    </div>
  </div>
</template>
<script>

import ImageContainer from "@/components/ImageContainer.vue";

export default {
  components: {ImageContainer},
  data() {
    return {
      paginaActual:0,
      fechaInicio:null,
      fechaFin:null,
      items: [],
      visibleItems: [],
      pageSize: 10,
      currentPage: 1,
      loading: false,
      selectedSource: "",
      selectedClass: "",
      options2: [],
      imagenDetalleIndex: null,
      masFiltros: false,
    };
  },
  created() {
    this.getImages()
  }
  ,
  setup() {
    const formatearClase = (valor) => {
      switch (valor) {
        case 'ave_volando':
          return 'Ave Volando';
        case 'ave_posada':
          return 'Ave Posada';
        case 'ave_rapaz_posada':
          return 'Rapaz Posada';
        case 'ave_rapaz_volando':
          return 'Rapaz volando';
          // Agrega más casos según sea necesario
        default:
          return 'ave (error)'; // Mantén el valor original si no coincide con ninguno de los casos
      }
    };
    return {
      formatearClase,
    };
  }
    ,
  methods: {
        async getImages() {
          if(this.selectedClass==="")
          {
            this.selectedClass='All'
          }
          if(this.fechaInicio===null) {
            if (!this.masFiltros)
            {
              this.fechaInicio = new Date();
              this.fechaInicio.setUTCFullYear(1970,1,1);
              this.fechaInicio.setHours(0,0,0);
            }
          }
          if(this.fechaFin===null)
          {
            this.fechaFin= new Date();
            this.fechaFin.setHours(23,59,59);
          }
          return await fetch("http://127.0.0.1:5000/getsAll", {
            headers: {
              'source': this.selectedSource,
              'class': this.selectedClass,
              'page':this.paginaActual,
              'beginning': this.fechaInicio.toISOString(),
              'end': this.fechaFin.toISOString(),
            },
            method: 'POST'
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
    changeMoreFilters() {

      this.masFiltros = !this.masFiltros;
    },
    nextPage()
    {
      this.paginaActual+=1;
      this.getImages()
    },
    previousPage() {
      this.paginaActual = this.paginaActual === 0 ? 0 : (this.paginaActual - 1)
      this.getImages()
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
  margin-right: 1%;
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
  background-color: rgba(0, 0, 0, 1);
  padding: 10px;
  text-align: center;
  z-index: 1; /* Para que el detalle esté encima de las otras imágenes */
  min-width: 250px;
  max-width: 90%; /* Ajusta el ancho máximo según sea necesario */
  max-height: 80%; /* Ajusta la altura máxima según sea necesario */
  overflow: auto; /* Agrega desplazamiento si la imagen es demasiado grande */
  border-radius: 10px; /* Bordes redondeados */
}

.responsive-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* Ajustar la imagen manteniendo su relación de aspecto */
}
.fila {
  min-width: 180px;
  width: 90%;
  display: flex;
  text-align: center;
  padding-left: 30%;

}

.letra-pequena {
  font-size: 20px;
  color: azure;
}

.margen-derecho {
  margin-right: 10px; /* Ajusta el espacio entre el primer y segundo P según sea necesario */
}

.contenedor-texto {
  display: flex;
  flex-direction: column;
  align-items: center; /* Centra horizontalmente */
  justify-content: space-between; /* Centra verticalmente */
  padding: 1%;
}

.input-container {
  position: relative;
  margin-bottom: 20px;
}

.input-container label {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  pointer-events: none;
  transition: top 0.3s ease-out;
  background-color: #fff;
  padding: 0 5px;
}

.input-container label.label-up {
  top: 0;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.filtros
{
  margin-right: 0.5%;
}

.boton-bonito {
  background-color: royalblue;
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.boton-bonito:hover {
  background-color: #45a049;
}

.boton-bonito:disabled {
  background-color: #ccc;
  color: #2c3e50;
  cursor: not-allowed;
}
</style>