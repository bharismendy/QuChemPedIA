<template>
  <div class="col">
    <transition-group
      name="fadeUp"
    >
      <b-alert
        v-for="notif in notifications"
        :key="notif.id"
        style="animation-duration: 0.5s"
        :variant="notif.variant"
        :show="true"
      >
        {{ notif.message }}
      </b-alert>
    </transition-group>
  </div>
</template>

<script>
import eBus from '../event-bus'

export default {
  name: 'QcpiaNotificationStack',
  data () {
    return {
      notifications: [],
      lastId: 0
    }
  },
  mounted () {
    eBus.$on(eBus.signals.notify.SUCCESS, ({ message, timeout = 2000 }) => {
      this.pushNotification({ message, timeout, variant: 'success' })
    })

    eBus.$on(eBus.signals.notify.ERROR, ({ message, timeout = 2000 }) => {
      this.pushNotification({ message, timeout, variant: 'danger' })
    })
  },
  methods: {
    pushNotification ({ message, timeout, variant }) {
      const id = ++this.lastId
      this.notifications.push({
        message,
        variant,
        id
      })
      setTimeout(() => {
        const index = this.notifications.findIndex((elt) => elt.id === id)
        this.notifications.splice(index, 1)
      }, timeout)
    }
  }
}
</script>

<style scoped>

</style>
