<template>
  <transition name="fade" mode="out-in">
    <div v-if="isLoading" key="loading">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>
    <div v-else key="content">
      <div class="container">
        <div class="row">
          <div  class="col order-5">
            <div v-show="alertConfig.show" class="alertContainer">
              <alert
                  :show="alertConfig.show"
                  :type="alertConfig.type"
                  :message="alertConfig.message"
              ></alert>
            </div>
            <div id="formularioyimagen">
              <h1 id="textoAlerta">{{name}} un ave rapaz fue detectada id imagen:{{$route.params.id}}</h1>
              <img id="imagen" :src="img" alt="alt"/>
              <br/>
              <hr class="hr" />
              <br/>
              <div class=".col-md-4">
                <h4>¿Considera la deteccion Correcta?</h4>
                <div id="formulario">
                  <form v-on:submit.prevent>
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
                      <button type="submit" class="btn btn-primary" v-on:click="send">Enviar</button>
                      <br/>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import Alert from "@/components/Alert.vue";
export default {
  name: "RaptorDetected",
  components: {Alert},
  comments:{
    Alert
  },
  data: () =>({
    id:-1,
    img: "",
    alt: "",
    comentario:"",
    correcto:0, //recordar que 1 es correcto y 0 es incorrecto
    alertConfig: {
      show: false,
      type: "",
      message: ""
    },
    isLoading: true
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
          return  await fetch("http://127.0.0.1:5000/imagen",{
            method: 'POST',
            headers: {
              'id': this.$route.params.id
            }
          }).then(response =>
          {
            return response.json()
          }).then(jsonResponse=>
          {
            this.img=jsonResponse.url
            this.id=jsonResponse.id
            this.isLoading=false
          }).catch( () =>
          {
            this.alertConfig.show = true;
            this.alertConfig.type = "error";
            this.alertConfig.message = "Ocurrio un error al cargar la imagen"
            this.isLoading=false

          })
        },
        async send()
        {
          return  await fetch("http://127.0.0.1:5000/save_validation",{
            method: 'POST',
            headers: {
              'idDetection': this.id,
              'selectedOption':this.correcto,
              'comments':this.comentario
            }
          }).then(() =>
          {
            alert('datos guardados')
          }).catch( () =>
          {
            alert('error datos no guardados')

          })
        }
      }
}
</script>

<style scoped>

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
.alertContainer
{
  align-content: center;
  width: 90%;
  margin-left: 2%;
  margin-right: 2%;
}
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

#imagen
{
  max-width: 80%;
  max-height: 70%;
}
</style>
