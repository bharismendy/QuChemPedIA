<template>
  <div
    ref="container"
    class="w-100"
  >
    <b-btn
      variant="primary"
      @click="toggleViz"
    >
      Toggle visualisation
    </b-btn>
    <iframe
      v-if="displayJsmol"
      :src="vizUrl"
      class="w-100 border-0"
      height="500"
    />
  </div>
</template>

<script>
export default {
  name: 'QcpiaMoleculeVizJsMol',
  props: {
    metadata: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      displayJsmol: false
    }
  },
  computed: {
    vizUrl () {
      return `${this.$root.baseUrl}/access/viz?log_file=${this.metadata.log_file}`
    }
  },
  methods: {
    toggleViz () {
      this.displayJsmol = !this.displayJsmol
    }
  }
}
</script>

<style scoped>

</style>
