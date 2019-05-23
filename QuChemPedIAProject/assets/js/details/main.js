import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import QcpiaDetails from './components/QcpiaDetails.vue'
import eBus from '../event-bus'

Vue.use(BootstrapVue)

const appElement = document.querySelector('#app')

window.qcpia = window.qcpia ? window.qcpia : {}

const baseUrl = window.qcpia.baseUrl ? window.qcpia.baseUrl : 'http://localhost:8000/'

if (appElement) {
  const id = appElement.dataset.moleculeid
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

function jmolInitViz (fileUrl) {
  console.log('jmolInitViz')
  const Info = {
    use: 'HTML5',
    width: '500',
    height: '500',
    debug: false,
    color: '0xC0C0C0',
    j2sPath: '/common_qcpia/static/js/jsmol/j2s',
    isSigned: 'true',
    disableJ2SLoadMonitor: true,
    disableInitialConsole: true,
    addSelectionOptions: false,
    serverURL: 'https://chemapps.stolaf.edu/jmol/jsmol/php/jsmol.php',
    // readyFunction: setOptions,
    script: `set zoomLarge falase; load ${fileUrl}`
  }

  window.Jmol._document = null
  window.$('#apphere').html(window.Jmol.getAppletHtml('jmolApplet0', Info))
}

let vizInitialized = false

eBus.$on(eBus.signals.tabs.SWITCH, ({ name, data }) => {
  const vizContainer = window.$('#vizContainer')
  if (name === 'viz') {
    vizContainer.show()
    if (!vizInitialized) {
      const fileUrl = '/common_qcpia/static/data_dir/file_step_0.log'
      jmolInitViz(fileUrl) // TODO retrieve file id
      vizInitialized = true
    }
  } else {
    vizContainer.hide()
  }
})
