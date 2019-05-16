<template>
  <b-tabs
    pills
    vertical
    card
  >
    <b-tab
      v-if="displayWaveFunction"
      title="Wavefunction"
    >
      <qcpia-molecule-results-wavefunction
        :molecule="molecule"
        :results="results"
      />
    </b-tab>
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
      v-if="displayGeometry"
      title="Geometry"
    >
      <qcpia-molecule-results-geometry
        :molecule="molecule"
        :results="results"
        :computational-details="computationalDetails"
      />
    </b-tab>
    <b-tab
      v-if="displayExcitedStates"
      title="Excited States"
    >
      <b-card-text>
        TODO
      </b-card-text>
    </b-tab>
  </b-tabs>
</template>

<script>
import { isObjectEmpty } from '../../utils'
import QcpiaMoleculeResultsThermochemistry from './QcpiaMoleculeResultsThermochemistry.vue'
import QcpiaMoleculeResultsGeometry from './QcpiaMoleculeResultsGeometry.vue'
import QcpiaMoleculeResultsWavefunction from './QcpiaMoleculeResultsWavefunction.vue'

export default {
  name: 'QcpiaMoleculeResults',
  components: {
    QcpiaMoleculeResultsWavefunction,
    QcpiaMoleculeResultsGeometry,
    QcpiaMoleculeResultsThermochemistry
  },
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
    displayWaveFunction () {
      return this.results.wavefunction && !isObjectEmpty(this.results.wavefunction)
    },
    displayThermochemistry () {
      return this.results.freq && !isObjectEmpty(this.results.freq)
    },
    displayGeometry () {
      return this.results.geometry && !isObjectEmpty(this.results.geometry)
    },
    displayExcitedStates () {
      return this.results.excited_states && !isObjectEmpty(this.results.excited_states)
    }
  }
}
</script>

<style scoped>

</style>
