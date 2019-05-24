<template>
  <div>
    <b-tabs
      v-if="tabsDisplay"
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
        <qcpia-molecule-results-excited-states
          :results="results"
        />
      </b-tab>
    </b-tabs>
    <template v-else>
      <div
        v-if="displayWaveFunction"
        class="mt-2 pb-3 border-bottom"
      >
        <h4>Wavefunction</h4>
        <qcpia-molecule-results-wavefunction
          :molecule="molecule"
          :results="results"
        />
      </div>
      <div
        v-if="displayGeometry"
        class="mt-2 pb-3 border-bottom"
      >
        <h4>Geometry</h4>
        <qcpia-molecule-results-geometry
          :molecule="molecule"
          :results="results"
          :computational-details="computationalDetails"
        />
      </div>
      <div
        v-if="displayExcitedStates"
        class="mt-2 pb-3 border-bottom"
      >
        <h4>Excited States</h4>
        <qcpia-molecule-results-excited-states
          :results="results"
        />
      </div>
    </template>
  </div>
</template>

<script>
import { isObjectEmpty } from '../../utils'
import QcpiaMoleculeResultsThermochemistry from './QcpiaMoleculeResultsThermochemistry.vue'
import QcpiaMoleculeResultsGeometry from './QcpiaMoleculeResultsGeometry.vue'
import QcpiaMoleculeResultsWavefunction from './QcpiaMoleculeResultsWavefunction.vue'
import QcpiaMoleculeResultsExcitedStates from './QcpiaMoleculeResultsExcitedStates.vue'

export default {
  name: 'QcpiaMoleculeResults',
  components: {
    QcpiaMoleculeResultsExcitedStates,
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
    },
    tabsDisplay: {
      type: Boolean,
      required: false,
      default: true
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
