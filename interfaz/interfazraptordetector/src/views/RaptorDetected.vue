<template>
  <div class="container">
    <div class="row">
      <div  class="col order-5">
        <div id="formularioyimagen">
          <h1 id="textoAlerta">{{name}} un ave rapaz fue detectada id imagen:{{$route.params.id}}</h1>
          <img style="width: 80%" :src="img" alt="alt"/>
          <br/>
          <hr class="hr" />
          <br/>
          <div class=".col-md-4">
            <h4>¿Considera la deteccion Correcta?</h4>
            <div id="formulario">
              <form>
                <div class="mb-3">
                  <div class="form-check">
                    <input v-model="correcto" value="1" class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
                    <label class="form-check-label" for="flexRadioDefault1">
                      Deteccion correcta.
                    </label>
                  </div>
                </div>
                <div class="mb-3">
                  <div class="form-check">
                    <input v-model="correcto" value="0" class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                    <label class="form-check-label" for="flexRadioDefault2">
                      Deteccion incorrecta.
                    </label>
                  </div>
                </div>
                <div class="form-floating">
                  <textarea v-model="comentario" class="form-control" placeholder="Leave a comment here" id="floatingTextarea2" style="height: 100px"></textarea>
                  <label for="floatingTextarea2">Comentarios</label>
                </div>
                <div>
                  <br/>
                  <button type="submit" class="btn btn-primary">Enviar</button>
                  <br/>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "RaptorDetected",
  data: () =>({
    img: "",
    alt: "",
    comentario:"",
    correcto:0 //recordar que 1 es correcto y 0 es incorrecto

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
        },
        changeCorrecto()
        {
          if (this.correcto===1)
          {
            this.correcto=0
          }
          else
          {
            this.correcto=1
          }
        }
      }
}
</script>

<style scoped>
#formularioyimagen
{
  align-content: center;
  padding-top: 5%;
  width: 90%;
  margin-left: 2%;
  margin-right: 2%;
  border: 1px solid #ccc;
  box-shadow: 7px 7px 7px #3A6670;
  margin-bottom: 5%;
  padding-bottom: 2%;
}

#textoAlerta
{
  font-size: 3vw;
}
#formulario
{
  padding-left: 10%;
  margin-top: 2%;
  width: 90%;
  alignment: center;
  text-align: left;
}
</style>
