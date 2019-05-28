<template>
  <div class="container">
    <div class="row text-primary">
      <div
        class="col col-lg-6"
        data-testid="molecule_formula"
      >
        <h2
          v-html="formattedFormula"
        />
      </div>
      <div
        v-if="molecule.iupac"
        class="col col-lg-6"
      >
        <h2>{{ molecule.iupac }}</h2>
      </div>
    </div>
    <div
      class="row"
      style="font-size: 1rem"
    >
      <div class="col-12 col-lg-6">
        <div class="row align-items-center">
          <a
            v-b-tooltip.hover
            class="col-auto text-muted"
            title="International Chemical Identifier"
            href="https://en.wikipedia.org/wiki/International_Chemical_Identifier"
          >Inchi
          </a>
          <div
            v-b-tooltip.hover
            class="col text-left"
            data-testid="molecule_inchi"
            style="text-overflow: ellipsis;  white-space: nowrap;overflow: hidden;"
            :title="molecule.inchi.slice(6)"
          >
            {{ molecule.inchi.slice(6) }}
          </div>
          <div
            class="col-auto text-left"
          >
            <qcpia-copy-text-button
              :text="molecule.inchi.slice(6)"
              tooltip-text="Copy Inchi to clipboard"
              size="sm"
              variant="outline-primary"
              class="text-center"
              @copied="notifyCopy"
            />
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="row">
          <a
            v-b-tooltip.hover
            class="col-auto text-muted"
            title="Simplified Molecular Input Line Entry Specification"
            href="https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_Specification"
          >SMILES
          </a>
          <div
            v-b-tooltip.hover
            class="col text-left"
            data-testid="molecule_inchi"
            style="text-overflow: ellipsis;  white-space: nowrap;overflow: hidden;"
            :title="molecule.can"
          >
            {{ molecule.can }}
          </div>
          <div
            class="col-auto text-left"
          >
            <qcpia-copy-text-button
              :text="molecule.can"
              tooltip-text="Copy SMILES to clipboard"
              size="sm"
              variant="outline-primary"
              class="text-center"
              @copied="notifyCopy"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="row justify-content-center">
      <div
        class="col-lg-6 col-md-12"
        style="overflow: hidden "
      >
        <qcpia-molecule-smiles
          v-if="molecule.can"
          :smiles="molecule.can"
          class="mt-n4"
        />
      </div>
    </div>
    <div class="row justify-content-around flex-row-reverse">
      <div class="col-lg-6 col-md-12">
        <h5 class="border-bottom pb-1">
          Molecule Details
        </h5>

        <qcpia-molecule-molecule
          :molecule="molecule"
          :hidden-props="['inchi', 'can', 'iupac']"
        />

        <h5 class="border-bottom pb-1 mt-2">
          Authorship
        </h5>
        <qcpia-molecule-authorship
          :metadata="metadata"
          :author-repository="authorRepository"
        />
      </div>
      <div class="col-lg-6 col-md-12">
        <h5 class="border-bottom mt-3 mt-lg-0 pb-1  ">
          Computation details
        </h5>
        <qcpia-molecule-computational-details
          :computational-details="computationalDetails"
          :job-types="jobTypes"
        />
      </div>
    </div>
  </div>
</template>

<script>

import eBus from '../../event-bus'
import { moleculeFormulaToHtml } from '../../utils'
import AuthorRepository from '../../api/AuthorRepository'
// VueJS components
import QcpiaMoleculeSmiles from './QcpiaMoleculeSmiles.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaMoleculeMolecule from './QcpiaMoleculeMolecule.vue'
import QcpiaCopyTextButton from './QcpiaCopyTextButton.vue'
import QcpiaMoleculeAuthorship from './QcpiaMoleculeAuthorship.vue'

// This component display the main information about a molecule : formula, charge, inchi ...
export default {
  name: 'QcpiaMoleculeAbstract',
  components: {
    QcpiaMoleculeAuthorship,
    QcpiaMoleculeMolecule,
    QcpiaMoleculeComputationalDetails,
    QcpiaMoleculeSmiles,
    QcpiaCopyTextButton
  },
  // data () {return {}}
  props: {
    // The molecule to display
    molecule: {
      type: Object,
      required: true
    },
    jobTypes: {
      type: Array,
      required: true
    },
    computationalDetails: {
      type: Object,
      required: true
    },
    metadata: {
      type: Object,
      required: true
    },
    authorRepository: {
      type: AuthorRepository,
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
  },
  methods: {
    notifyCopy () {
      eBus.$emit(eBus.signals.notify.SUCCESS, { message: 'Copied to clipboard' })
    }
  }
}
</script>

<style scoped>

</style>
