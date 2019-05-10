import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import QcpiaDetails from './components/QcpiaDetails.vue'

Vue.use(BootstrapVue)

const appElement = document.querySelector('#app')
if (appElement) {
  const id = appElement.dataset.moleculeid
  console.log(id)
  /* eslint-disable no-new */
  new Vue({
    el: '#app',
    components: { QcpiaDetails },
    template: `<QcpiaDetails id="${id}"/>`
  })
}
