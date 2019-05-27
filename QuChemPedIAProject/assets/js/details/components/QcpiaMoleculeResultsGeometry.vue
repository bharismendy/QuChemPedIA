<template>
  <div>
    <div
      v-if="results.geometry.nuclear_repulsion_energy_from_xyz"
      class="row"
    >
      <div class="col text-muted">
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
      <h5>Cartesian atomic coordinates</h5>
      <div class="row">
        <div class="col-12 col-lg p-2">
          <b-btn
            :variant="showAtomicCoordTable ? 'primary' : 'outline-primary'"
            @click="toogleCartesionAtomicCoordinatesTableDisplay"
          >
            {{ showAtomicCoordTable ? 'Hide' : 'Show' }} Cartesian atomic coordinates
          </b-btn>
        </div>
        <div class="col-12 col-lg p-2">
          <b-btn
            :href="downloadCartesianAtomicCoordinatesTableHref"
            :download="`molecule-${this.$root.moleculeId}.xyz`"
          >
            Download <i
              class="fa fa-download"
              aria-hidden="true"
            />
          </b-btn>
        </div>
      </div>
      <transition
        name="fade"
        enter-active-class="fadeInUp"
        leave-active-class="fadeOutDown"
      >
        <div
          v-show="showAtomicCoordTable"
          style="animation-duration: 0.5s"
        >
          <b-pagination
            v-model="atomicCoordTableCurrentPage"
            :total-rows="cartesianAtomicCoordinatesTableItems.length"
            :per-page="atomicCoordPerPage"
            align="center"
          />
          <p class="text-muted">
            Coordinates are shown in Angstroms
          </p>
          <b-table
            :current-page="atomicCoordTableCurrentPage"
            :per-page="atomicCoordPerPage"
            :items="cartesianAtomicCoordinatesTableItems"
          />
        </div>
      </transition>
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
      atomicCoordPerPage: 10,
      showAtomicCoordTable: false
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
    },

    downloadCartesianAtomicCoordinatesTableHref () {
      const tableString = `${this.cartesianAtomicCoordinatesTableItems.length}\n${this.$root.moleculeId}\tQuChemPedIA\n${
        this.cartesianAtomicCoordinatesTableItems.map((elt) => {
          return `${elt.atom}\t${elt.x}\t${elt.y}\t${elt.z}`
        }).join('\r\n')
      }`
      return 'data:text/plain;charset=utf-8,' + encodeURIComponent(tableString)
    }

  },
  methods: {
    toogleCartesionAtomicCoordinatesTableDisplay () {
      this.showAtomicCoordTable = !this.showAtomicCoordTable
    }
  }
}
</script>

<style scoped>

</style>
