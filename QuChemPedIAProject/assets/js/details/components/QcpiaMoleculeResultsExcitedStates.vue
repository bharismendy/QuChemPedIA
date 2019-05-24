<template>
  <div v-if="displaymonoElectronicExcitationTable">
    <h5>Calculated mono-electronic excitations</h5>
    <b-table
      :fields="monoElectronicExcitationTableFields"
      :items="monoElectronicExcitationTableData"
    />
  </div>
</template>

<script>
export default {
  name: 'QcpiaMoleculeResultsExcitedStates',
  props: {
    results: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      monoElectronicExcitationTableFields: [
        { key: 'number', label: 'Number' },
        { key: 'energyCm_n1' },
        { key: 'energy_nm', label: 'Energy (nm)' },
        { key: 'symmetry', label: 'Symmetry' },
        { key: 'oscillatorStrength', label: 'Oscillator Strength' },
        { key: 'rotatoryStrength', label: 'Rotatory strength' }
      ]
    }
  },
  computed: {
    displaymonoElectronicExcitationTable () {
      return this.results.excited_states.et_energies
    },
    monoElectronicExcitationTableData () {
      if (!this.results.excited_states.et_energies) return []

      const etEnergies = this.results.excited_states.et_energies
      const etSym = this.results.excited_states.et_sym
      const etOscs = this.results.excited_states.et_oscs
      const etRot = this.results.excited_states.et_rot

      return etEnergies.map((energy, index) => {
        return {
          number: index + 1,
          energyCm_n1: Math.round(energy),
          energy_nm: Math.round(10000000 / energy),
          symmetry: etSym[index],
          oscillatorStrength: etOscs[index].toFixed(4),
          rotatoryStrength: etRot[index] !== undefined && etRot !== null ? etRot[index].toFixed(4) : 'Unknown'
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
