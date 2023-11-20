import 'bootstrap/dist/css/bootstrap.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VModal from 'vue-js-modal'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

Vue.use(VModal,{ componentName: 'modal' })
import 'bootstrap/dist/js/bootstrap'
