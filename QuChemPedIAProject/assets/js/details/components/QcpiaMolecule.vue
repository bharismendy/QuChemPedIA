<template>
  <div>
    <QcpiaMoleculeAbstract :molecule="molecule" />
  </div>
</template>

<script>
import QcpiaMoleculeAbstract from './QcpiaMoleculeAbstract.vue'
export default {
  name: 'QcpiaMolecule',
  components: { QcpiaMoleculeAbstract },
  props: {
    molecule: {
      type: Object,
      required: true
    },
    metadata: {
      type: Object,
      required: true
    },
    results: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
