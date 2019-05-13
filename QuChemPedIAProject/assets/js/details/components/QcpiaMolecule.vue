<template>
  <div>
    <b-card class="mt-3">
      <h5 slot="header">
        Molecule
      </h5>
      <QcpiaMoleculeAbstract :molecule="molecule" />
    </b-card>
    <b-card class="mt-3">
      <h5 slot="header">
        Computational Details
      </h5>
      <qcpia-molecule-computational-details
        :computational-details="computationalDetails"
      />
    </b-card>
    <b-card class="mt-3">
      <h5 slot="header">
        Results
      </h5>
      <qcpia-molecule-results
        :molecule="molecule"
        :results="results"
      />
    </b-card>
  </div>
</template>

<script>
import QcpiaMoleculeAbstract from './QcpiaMoleculeAbstract.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaMoleculeResults from './QcpiaMoleculeResults.vue'

export default {
  name: 'QcpiaMolecule',
  components: { QcpiaMoleculeResults, QcpiaMoleculeComputationalDetails, QcpiaMoleculeAbstract },
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
