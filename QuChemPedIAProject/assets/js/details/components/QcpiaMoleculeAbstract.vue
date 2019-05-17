<template>
  <div class="container">
    <div class="row justify-content-center">
      <div
        class="col pl-3"
        data-testid="molecule_formula"
      >
        <h2
          class="text-primary"
          v-html="formattedFormula"
        />
        <div class="">
          <div class="d-flex">
            <span class="mr-2 text-muted">
              Charge :
            </span>
            <span
              class=""
              data-testid="molecule_charge"
            >
              {{ molecule.charge }}
            </span>
          </div>
          <div class="d-flex">
            <span
              class="mr-2 text-muted"
            >
              Spin Multiplicity :
            </span>
            <span
              class=""
              data-testid="molecule_multiplicity"
            >
              {{ molecule.multiplicity }}
            </span>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="">
          <span class="text-muted">Computed with </span> {{ software }}
        </div>
        <div class="row">
          <div class="col-12 col-lg-auto">
            <span class="text-muted">Method : </span> {{ computationalDetails.general.last_theory }}
          </div>
          <div class="col-12 col-lg-auto">
            <span class="text-muted">Functional : </span> {{ computationalDetails.general.functional }}
          </div>
        </div>
      </div>
    </div>

    <div class="row justify-content-center">
      <div
        class="col-lg-5 col-md-12"
        style="overflow: hidden "
      >
        <qcpia-molecule-smiles
          v-if="molecule.can"
          :smiles="molecule.can"
          class="mt-n4"
        />
      </div>
    </div>
    <div class="row justify-content-around">
      <div class="col-lg-5 col-md-12">
        <h5 class="border-bottom">
          Molecule Details
        </h5>

        <qcpia-molecule-molecule
          :molecule="molecule"
        />
      </div>
      <div class="col-lg-5 col-md-12">
        <h5 class="border-bottom mt-3 mt-lg-0">
          Computation details
        </h5>
        <qcpia-molecule-computational-details :computational-details="computationalDetails" />
      </div>
    </div>
  </div>
</template>

<script>
import QcpiaMoleculeSmiles from './QcpiaMoleculeSmiles.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaMoleculeMolecule from './QcpiaMoleculeMolecule.vue'
import { moleculeFormulaToHtml } from '../../utils'

// This component display the main information about a molecule : formula, charge, inchi ...
export default {
  name: 'QcpiaMoleculeAbstract',
  components: { QcpiaMoleculeMolecule, QcpiaMoleculeComputationalDetails, QcpiaMoleculeSmiles },
  // data () {return {}}
  props: {
    // The molecule to display
    molecule: {
      type: Object,
      required: true
    },
    computationalDetails: {
      type: Object,
      required: true
    }
  },
  computed: {
    /**
       * Render the html string for the molecule formula
       * @returns {null|String}
       */
    formattedFormula () {
      if (this.molecule.formula) {
        return moleculeFormulaToHtml(this.molecule.formula, this.molecule.charge)
      }
      return null
    },

    software () {
      const software = this.computationalDetails.general.package
      const softwareVersionStr = this.computationalDetails.general.package_version ? ' ( ' + this.computationalDetails.general.package_version + ' )' : ''
      return `${software}${softwareVersionStr}`
    }
  }
}
</script>

<style scoped>

</style>
