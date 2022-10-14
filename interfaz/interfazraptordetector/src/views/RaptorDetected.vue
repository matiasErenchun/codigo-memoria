<template>
  <div>
    <h1>{{name}} un ave paraz fue detectada id imagen:{{$route.params.id}}</h1>
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

</style>
