<template>
  <b-tabs
    pills
    vertical
    card
  >
    <b-tab
      v-if="displayThermochemistry"
      title="Thermochemistry"
    >
      <qcpia-molecule-results-thermochemistry
        :molecule="molecule"
        :results="results"
      />
    </b-tab>
    <b-tab
      title="Geometry"
      active
    >
      <qcpia-molecule-results-geometry
        :molecule="molecule"
        :results="results"
        :computational-details="computationalDetails"
      />
    </b-tab>
    <b-tab
      title="Excited States"
      active
    >
      <b-card-text>
        Content
      </b-card-text>
    </b-tab>
  </b-tabs>
</template>

<script>
import { isObjectEmpty } from '../../utils'
import QcpiaMoleculeResultsThermochemistry from './QcpiaMoleculeResultsThermochemistry.vue'
import QcpiaMoleculeResultsGeometry from './QcpiaMoleculeResultsGeometry.vue'

export default {
  name: 'QcpiaMoleculeResults',
  components: { QcpiaMoleculeResultsGeometry, QcpiaMoleculeResultsThermochemistry },
  props: {
    molecule: {
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
  },
  computed: {
    displayThermochemistry () {
      return this.results.freq && !isObjectEmpty(this.results.freq)
    },
    displayGeometry () {
      return this.results.geometry && !isObjectEmpty(this.results.geometry)
    }
  }
}
</script>

<style scoped>

</style>
