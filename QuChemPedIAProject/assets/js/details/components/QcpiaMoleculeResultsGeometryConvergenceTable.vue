<template>
  <div v-if="displayTable">
    <h5>Geometry optimization convergence criteria</h5>
    <p
      class="font-italic"
      v-html="description"
    />
    <b-table
      :items="tableItems"
      :fields="tableFields"
    />
  </div>
</template>

<script>
export default {
  name: 'QcpiaMoleculeResultsGeometryConvergenceTable',
  props: {
    results: {
      type: Object,
      required: true
    },
    computationalDetails: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      supportedSoftware: ['Gaussian']
    }
  },
  computed: {
    displayTable () {
      return this.tableItems !== null
    },
    tableItems () {
      if (!this.computationalDetails.general.package) return null

      const software = this.computationalDetails.general.package
      const method = `buildItems${software}`

      if (!this[method]) return null

      return this[method]()
    },
    tableFields () {
      if (!this.computationalDetails.general.package) return null

      const software = this.computationalDetails.general.package

      const method = `buildFields${software}`

      if (!this[method]) return null

      return this[method]()
    },
    description () {
      if (!this.computationalDetails.general.package) return null

      const software = this.computationalDetails.general.package

      const method = `buildDescription${software}`

      if (!this[method]) return null

      return this[method]()
    }
  },
  methods: {
    buildItemsGaussian () {
      const titreCol = ['Maximum Force', 'RMS Force', 'Maximum Displacement', 'RMS Displacement']
      const items = []

      if (!(this.computationalDetails.geometry.geometric_targets && this.results.geometry.geometric_values[this.results.geometry.geometric_values.length - 1])) return null

      const geometricTargets = this.computationalDetails.geometry.geometric_targets
      const geometricValues = this.results.geometry.geometric_values[this.results.geometry.geometric_values.length - 1]

      for (let i = 0; i < geometricTargets.length && i < titreCol.length; ++i) {
        items.push({
          title: titreCol[i],
          value: geometricValues[i].toFixed(6),
          threshold: geometricTargets[i].toFixed(6)
        })
      }
      return items
    },
    buildFieldsGaussian () {
      return [
        { key: 'title', label: '' },
        { key: 'value', label: 'Value' },
        { key: 'threshold', label: 'Threshold' }
      ]
    },
    buildDescriptionGaussian () {
      return 'This calculation is the result of a geometry optimization process.'
    }
  }
}
</script>

<style scoped>

</style>
