<template>
  <div>
    <div
      v-if="wavefunction.total_molecular_energy"
      class="row"
    >
      <div class="col text-muted">
        Total molecular energy
      </div>
      <div class="col">
        {{ wavefunction.total_molecular_energy }}
      </div>
    </div>
    <div
      v-if="homoIndexes.length > 0"
      class="row"
    >
      <div class="col text-muted">
        HOMO number
      </div>
      <div class="col">
        {{ homoNumber }}
      </div>
    </div>

    <div
      v-if="displayHomeEnergiesTable"
      class="mt-3"
    >
      <h5 class="font-weight-bold text-center">
        Calculated energies for the frontier molecular orbitals
      </h5>
      <b-table
        :items="homoEnergiesTableItems"
        small
        borderless
        class="text-center"
      />
    </div>
    <div
      v-if="displayMullikenAtomic"
      class="mt-3"
    >
      <h5 class="text-center font-weight-bold">
        Most intense Mulliken atomic charges
      </h5>
      <p class="text-center">
        mean={{ mullikenChargesMean.toFixed(3) }}, e, std= {{ mullikenChargesStd.toFixed(3) }}
      </p>

      <b-table
        :items="mullikenAtomicItems"
        :fields="mullikenPartialChargeTableFields"
        class="text-center"
      />
    </div>
  </div>
</template>

<script>
import AtomSymbols from '../atom-symbols'

export default {
  name: 'QcpiaMoleculeResultsWavefunction',
  props: {
    results: {
      type: Object,
      required: true
    },
    molecule: {
      type: Object,
      required: true
    }

  },
  data () {
    return {
      homoEnergiesTableFields: [
        { key: 'homo-1', label: 'HOMO-1' },
        { key: 'homo', label: 'HOMO' },
        { key: 'lumo', label: 'LUMO' },
        { key: 'lumo+1', label: 'LUMO+1' }
      ],

      mullikenPartialChargeTableFields: [
        { key: 'symbol', label: 'Atom' },
        { key: 'index', label: 'Number' },
        { key: 'mullikenPartialCharge', label: 'Mulliken partial charges' }
      ]
    }
  },
  computed: {
    wavefunction () {
      return this.results.wavefunction || {}
    },

    homoIndexes () {
      return this.wavefunction.homo_indexes
        ? this.wavefunction.homo_indexes
        : []
    },

    homoNumber () {
      return this.homoIndexes.map(i => i + 1).join(', ')
    },

    displayHomeEnergiesTable () {
      return this.homoIndexes &&
          this.homoIndexes.length > 0 &&
          this.wavefunction.MO_energies &&
          this.wavefunction.MO_energies.length > 0
    },

    homoEnergiesTableItems () {
      if (!this.displayHomeEnergiesTable) return []

      const MoEnergies = this.wavefunction.MO_energies

      const items = []
      for (let j = 0; j < this.homoIndexes.length; ++j) {
        if (this.homoIndexes[j] <= 0) {
          items.push({
            'homo-1': 'N/A',
            'homo': MoEnergies[j][this.homoIndexes[j]].toFixed(2),
            'lumo': MoEnergies[j][this.homoIndexes[j] + 1].toFixed(2),
            'lumo+1': 'N/A'
          })
        } else {
          items.push({
            'homo-1': MoEnergies[j][this.homoIndexes[j] - 1].toFixed(2),
            'homo': MoEnergies[j][this.homoIndexes[j]].toFixed(2),
            'lumo': MoEnergies[j][this.homoIndexes[j] + 1].toFixed(2),
            'lumo+1': MoEnergies[j][this.homoIndexes[j] + 2].toFixed(2)
          })
        }
      }
      return items
    },

    mullikenPartialCharges () {
      return this.wavefunction.Mulliken_partial_charges || []
    },

    displayMullikenAtomic () {
      return this.mullikenPartialCharges.length > 0
    },

    mullikenAtomicItems () {
      const items = []

      for (let j = 0; j < this.mullikenPartialCharges.length; ++j) {
        items.push({
          symbol: AtomSymbols[this.molecule.atoms_Z[j] - 1],
          index: j + 1,
          mullikenPartialCharge: this.mullikenPartialCharges[j]
        })
      }

      items.sort((a, b) => a.mullikenPartialCharge - b.mullikenPartialCharge)

      const thresholdMax = this.mullikenChargesMean + this.mullikenChargesStd
      const thresholdMin = this.mullikenChargesMean - this.mullikenChargesStd

      if (items.length < 5) {
        return items
      } else {
        return items.filter(item => item.mullikenPartialCharge > thresholdMax || item.mullikenPartialCharge < thresholdMin)
      }
    },
    mullikenChargesMean () {
      // The reduce call return the sum of all elements in the array
      return this.mullikenPartialCharges.reduce((acc, curr) => acc + curr, 0) / this.mullikenPartialCharges.length
    },

    mullikenChargesStd () {
      return Math.sqrt(
        this.mullikenPartialCharges.reduce((acc, curr) => acc + Math.pow(curr - this.mullikenChargesMean, 2)) / this.mullikenPartialCharges.length
      )
    }
  }
}
</script>

<style scoped>

</style>
