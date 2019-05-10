<template>
  <div>
    <QcpiaMoleculeAbstract :molecule="molecule" />

    <qcpia-molecule-computational-details
      class="mt-4"
      :computational-details="computationalDetails"
    />
  </div>
</template>

<script>
import QcpiaMoleculeAbstract from './QcpiaMoleculeAbstract.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'

export default {
  name: 'QcpiaMolecule',
  components: { QcpiaMoleculeComputationalDetails, QcpiaMoleculeAbstract },
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
    },
    computationalDetails: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
