// See https://alligator.io/vuejs/global-event-bus/

import Vue from 'vue'

export default new Vue({
  data: {
    signals: {
      notify: {
        SUCCESS: 'NOTIFY_SUCCESS',
        ERROR: 'NOTIFY_ERROR'
      },
      tabs: {
        SWITCH: 'TAB_SWITCH'
      }
    }
  }
})
