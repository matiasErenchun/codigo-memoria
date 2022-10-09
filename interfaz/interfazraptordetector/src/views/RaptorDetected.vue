<template>
  <h1>{{name}} un ave paraz fue detectada id imagen:{{$route.params.id}}</h1>
</template>

<script>
export default {
  name: "RaptorDetected",
  computed:
      {
        name()
        {
          return this.$route.query.name
        }
      }
}
</script>

<style scoped>

</style>
