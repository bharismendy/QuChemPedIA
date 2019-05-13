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
      <b-card-text>
        Content
      </b-card-text>
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
export default {
  name: 'QcpiaMoleculeResults',
  components: { QcpiaMoleculeResultsThermochemistry },
  props: {
    molecule: {
      type: Object,
      required: true
    },
    results: {
      type: Object,
      required: true
    }
  },
  computed: {
    displayThermochemistry () {
      return this.results.freq && !isObjectEmpty(this.results.freq)
    }
  }
}
</script>

<style scoped>

</style>
