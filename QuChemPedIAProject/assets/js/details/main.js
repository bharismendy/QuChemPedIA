import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import QcpiaDetails from './components/QcpiaDetails.vue'

Vue.use(BootstrapVue)

const appElement = document.querySelector('#app')

window.qcpia = window.qcpia ? window.qcpia : {}

const baseUrl = appElement.dataset.baseUrl
const dataDir = appElement.dataset.dataDir
if (appElement) {
  const id = appElement.dataset.moleculeid
  /* eslint-disable no-new */
  new Vue({
    el: '#app',
    components: { QcpiaDetails },
    data: {
      moleculeId: id,
      baseUrl,
      dataDir
    },
    template: `<QcpiaDetails id="${id}" base-url="${baseUrl}"/>`
  })
}
