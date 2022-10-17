<template>
  <div id="formularioyimagen">
    <h1 id="textoAlerta">{{name}} un ave rapaz fue detectada id imagen:{{$route.params.id}}</h1>
    <img style="width: 80%" :src="img" alt="alt"/>
  </div>
</template>

<script>
export default {
  name: "RaptorDetected",
  data: () =>({
    img: "",
    alt: ""
  }),
  computed:
      {
        name()
        {
          return this.$route.query.name
        }
      },
  created()
  {
    this.gentimagen()
  },
  methods:
      {
        async gentimagen()
        {
          const datos = await fetch("http://127.0.0.1:5000/imagen",{
            method: 'POST',
            headers: {
              'id': this.$route.params.id
            }
          })
          const respuesta = await datos.json()

          console.log(respuesta.url)
          this.img=respuesta.url
        }
      }
}
</script>

<style scoped>
#formularioyimagen
{
  padding-top: 5%;
  width: 90%;
  margin-left: 2%;
  margin-right: 2%;
  border: 1px solid #ccc;
  box-shadow: 7px 7px 7px #3A6670
}

#textoAlerta
{
  font-size: 3vw;
}
</style>
