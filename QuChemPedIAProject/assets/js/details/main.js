import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import QcpiaDetails from './components/QcpiaDetails.vue'

Vue.use(BootstrapVue)

const appElement = document.querySelector('#app')

window.qcpia = window.qcpia ? window.qcpia : {}

const baseUrl = window.qcpia.baseUrl ? window.qcpia.baseUrl : 'http://localhost:8000/'

if (appElement) {
  const id = appElement.dataset.moleculeid
  console.log({ id, baseUrl })
  /* eslint-disable no-new */
  new Vue({
    el: '#app',
    components: { QcpiaDetails },
    data: {
      moleculeId: id
    },
    template: `<QcpiaDetails id="${id}" base-url="${baseUrl}"/>`
  })
}
