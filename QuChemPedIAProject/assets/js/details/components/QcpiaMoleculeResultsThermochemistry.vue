<template>
  <div>
    <p class="font-italic">
      All values was calculated at 298.150000 K in atomic units.
    </p>
    <qcpia-data-map-presenter :data="tableData" />
    <b-table
      v-if="displayVibrationalTable"
      :items="vibrationalTableItems"
      responsive
    >
      <template
        slot="HEAD_frequencies"
        slot-scope="data"
      >
        <span v-html="data.label" />
      </template>
    </b-table>
  </div>
</template>

<script>
import QcpiaDataMapPresenter from './QcpiaDataMapPresenter.vue'
import tableDataMapHelper from '../mixins/tableDataMapHelpers'

export default {
  name: 'QcpiaMoleculeResultsThermochemistry',
  components: { QcpiaDataMapPresenter },
  mixins: [tableDataMapHelper],
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
  data () {
    return {
      tableDataDef: [
        {
          path: 'freq.zero_point_energy',
          label: 'Sum of electronic and zero-point energy'
        },
        {
          path: 'freq.electronic_thermal_energy',
          label: 'Sum of electronic and thermal'
        },
        {
          path: 'freq.entropy',
          label: 'Entropy'
        },
        {
          path: 'freq.enthalpy',
          label: 'Enthalpy'
        },
        {
          path: 'freq.free_energy',
          label: 'Gibbs free energy'
        }
      ],
      vibrationalTableFields: [
        {
          key: 'frequencies',
          label: 'Frequencies (cm<sup>-1</sup>)'
        },
        {
          key: 'intensity',
          label: 'Intensity (km/mol)'
        },
        {
          key: 'symmetry',
          label: 'Symmetry'
        }
      ]
    }
  },
  computed: {
    tableData () {
      // method defined in tableDataMapHelper mixin
      return this.buildTableData(this.tableDataDef, this.results)
    },
    displayVibrationalTable () {
      return this.results.freq.vibrational_int &&
          (this.results.freq.vibrational_int < 5 ||
            this.results.freq.vibrational_int > 20)
    },
    vibrationalTableItems () {
      if (!this.displayVibrationalTable) return []

      const freq = this.results.freq.vibrational_freq
      const int = this.results.freq.vibrational_int
      const sym = this.results.freq.vibrational_sym

      return int.map((elt, index) => {
        return {
          frequencies: freq[index],
          intensity: int[index],
          symmetry: sym[index]
        }
      })
    }
  }
}
</script>
