<template>
  <div
    ref="container"
    class="w-100"
  >
    <iframe
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
  computed: {
    vizUrl () {
      return `${this.$root.baseUrl}/access/viz?log_file=${this.metadata.log_file}`
    }
  }
}
</script>

<style scoped>

</style>
