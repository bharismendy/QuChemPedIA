<template>
  <div>
    <div
      v-if="results.geometry.nuclear_repulsion_energy_from_xyz"
      class="row"
    >
      <div class="col font-weight-bold">
        Nuclear repulsion energy in atomic units
      </div>
      <div class="col">
        {{ results.geometry.nuclear_repulsion_energy_from_xyz }}
      </div>
    </div>

    <qcpia-molecule-results-geometry-convergence-table
      class="mt-3"
      :results="results"
      :computational-details="computationalDetails"
    />

    <div
      v-if="displayCartesionAtomicCoordinates"
      class="mt-3"
    >
      <h6>Cartesian atomic coordinates in Angstroms</h6>
      <b-pagination
        v-model="atomicCoordTableCurrentPage"
        :total-rows="cartesianAtomicCoordinatesTableItems.length"
        :per-page="atomicCoordPerPage"
        align="center"
      />
      <b-table
        :current-page="atomicCoordTableCurrentPage"
        :per-page="atomicCoordPerPage"
        :items="cartesianAtomicCoordinatesTableItems"
      />
    </div>
  </div>
</template>

<script>
import AtomSymbols from '../atom-symbols'
import QcpiaMoleculeResultsGeometryConvergenceTable from './QcpiaMoleculeResultsGeometryConvergenceTable.vue'
export default {
  name: 'QcpiaMoleculeResultsGeometry',
  components: { QcpiaMoleculeResultsGeometryConvergenceTable },
  props: {
    results: {
      type: Object,
      required: true
    },
    molecule: {
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
      atomicCoordTableCurrentPage: 1,
      atomicCoordPerPage: 20
    }
  },
  computed: {
    displayCartesionAtomicCoordinates () {
      return this.results.geometry.elements_3D_coords_converged
    },

    cartesianAtomicCoordinatesTableItems () {
      const elements3dCoordsConverged = this.results.geometry.elements_3D_coords_converged
      const atomsZ = this.molecule.atoms_Z

      const table = []
      for (let i = 0; i < elements3dCoordsConverged.length; i += 3) {
        table.push({
          atom: AtomSymbols[atomsZ[i / 3] - 1],
          x: elements3dCoordsConverged[i],
          y: elements3dCoordsConverged[i + 1],
          z: elements3dCoordsConverged[i + 2]
        })
      }
      return table
    }
  }
}
</script>

<style scoped>

</style>
