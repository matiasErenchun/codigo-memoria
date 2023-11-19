
<template>
  <div class="ImageContainer">
    <img :src="imageSrc" class="responsive-image">
    <div class="contenedor-texto">
      <div class="fila">
        <p class="letra-pequena margen-derecho">Id: {{id}}</p>
        <p class="letra-pequena"> Clase: {{ formatearClase(classDetection)}}</p>
      </div>
      <div class="fila">
        <p class="letra-pequena">Fecha deteccion: {{formatearFecha(dateDetection)}}</p>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: {
    id: String,
    imageSrc:String,
    classDetection: String,
    dateDetection:String,
  },
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
    const formatearFecha=(fechaString)=>{
      // Convertir el string a un objeto Date
      const fecha = new Date(fechaString);

      // Obtener los componentes individuales de la fecha
      const dia = fecha.getDate().toString().padStart(2, '0');
      const mes = (fecha.getMonth() + 1).toString().padStart(2, '0');
      const anio = fecha.getFullYear();

      // Formatear la fecha en el formato deseado
      const fechaFormateada = `${dia}/${mes}/${anio}`;

      return fechaFormateada;
    }

    return {
      formatearFecha,
      formatearClase,
    };
  },
};
</script>

<style scoped>
.ImageContainer
{
  min-width: 250px;
  min-height: 75px;
  max-height: 100%;
  max-width: 100%;
  justify-content: center; /* Centrar contenido horizontalmente */
  align-items: center;
  background-color: #2c3e50;
  border:2px solid #2c3e50;
}
.responsive-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* Ajustar la imagen manteniendo su relación de aspecto */
}

.contenedor-texto {
  display: flex;
  flex-direction: column;
  align-items: center; /* Centra horizontalmente */
  justify-content: center; /* Centra verticalmente */
  padding: 5%;
}

.fila {
  min-width: 180px;
  width: 90%;
  display:flex;
  text-align: left;
}

.letra-pequena {
  font-size: 14px;
  color: azure;
}

.margen-derecho {
  margin-right: 10px; /* Ajusta el espacio entre el primer y segundo P según sea necesario */
}


</style>