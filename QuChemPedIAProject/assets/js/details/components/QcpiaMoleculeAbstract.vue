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
          <span class="text-muted">Computed with </span> {{ software }}
        </div>
        <div class="">
          <div class="d-inline-block">
            <span class="text-muted">Method : </span> {{ computationalDetails.general.last_theory }}
          </div>
          <div class="d-inline-block ml-2">
            <span class="text-muted">Functional : </span> {{ computationalDetails.general.functional }}
          </div>
        </div>
      </div>
      <div class="col">
        <div class="row justify-content-between">
          <div class="col-12 justify-content-between text-center">
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
          <div class="col-12 text-center">
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
        <div
          v-if="molecule.monoisotopic_mass"
          class="row mt-1"
        >
          <div class="col">
            <span class="text-muted">Monoisotopic mass</span>
          </div>
          <div
            class="col"
            data-testid="molecule_monoisotopic_mass"
          >
            {{ molecule.monoisotopic_mass }}
          </div>
        </div>

        <div
          v-if="molecule.iupac"
          class="row mt-1"
        >
          <div class="col row">
            <div class="">
              <span class="text-muted mr-2">Iupac</span>
              <qcpia-help-badge-link
                href="https://en.wikipedia.org/wiki/Union_internationale_de_chimie_pure_et_appliqu%C3%A9e"
                tooltip-text="International Union of Pure and Applied Chemistry"
                target="_blank"
              />
            </div>
            <div data-testid="molecule_iupac">
              {{ molecule.iupac }}
            </div>
          </div>
        </div>
        <div
          v-if="molecule.inchi"
          class="row mt-1"
        >
          <div class="col">
            <div class="row">
              <span class="col text-muted">Inchi
                <qcpia-help-badge-link
                  class="ml-2"
                  href="https://en.wikipedia.org/wiki/International_Chemical_Identifier"
                  tooltip-text="International Chemical Identifier"
                  target="_blank"
                /></span>
            </div>
            <div class="row">
              <div
                v-b-tooltip.hover
                class="col"
                data-testid="molecule_inchi"
                style="text-overflow: ellipsis;  white-space: nowrap;overflow: hidden;"
                :title="molecule.inchi.slice(6)"
                @click="copyInchi"
              >
                {{ molecule.inchi.slice(6) }}
              </div>
              <div
                class="col-1"
              >
                <qcpia-copy-text-button
                  :text="molecule.inchi.slice(6)"
                  tooltip-text="Copy"
                  class="p-1"
                  @copied="notifyCopy"
                />
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="molecule.can"
          class="row mt-1"
        >
          <div class="col">
            <div class="row">
              <span class="col text-muted">Canonical SMILES
                <qcpia-help-badge-link
                  href="https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_Specification"
                  tooltip-text="Simplified Molecular Input Line Entry Specification"
                  target="_blank"
                  class="ml-2"
                />
              </span>
            </div>
            <div class="row">
              <div
                v-b-tooltip.hover
                class="col"
                data-testid="molecule_can"
                style="text-overflow: ellipsis;  white-space: nowrap;overflow: hidden;"
                :title="molecule.can"
              >
                {{ molecule.can }}
              </div>
              <div class="col-1">
                <qcpia-copy-text-button
                  :text="molecule.can"
                  tooltip-text="Copy to clipboard"
                  class="p-1"
                  @copied="notifyCopy"
                />
              </div>
            </div>
          </div>
        </div>
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
import QcpiaHelpBadgeLink from './QcpiaHelpBadgeLink.vue'
import QcpiaMoleculeSmiles from './QcpiaMoleculeSmiles.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaCopyTextButton from './QcpiaCopyTextButton.vue'
import eBus from '../../event-bus'

// This component display the main information about a molecule : formula, charge, inchi ...
export default {
  name: 'QcpiaMoleculeAbstract',
  components: { QcpiaCopyTextButton, QcpiaMoleculeComputationalDetails, QcpiaHelpBadgeLink, QcpiaMoleculeSmiles },
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
        const charge = this.molecule.charge
        const formula = this.molecule.formula
        let formattedFormula = ''
        for (let i = formula.length - 1; i >= 0; i--) {
          if (i === formula.length - 1 && charge !== 0) {
            if (charge > 1 || charge < -1) {
              formattedFormula = formula.charAt(i - 1).sup() + formula.charAt(i).sup() + formattedFormula
              i--
            } else {
              formattedFormula = formula.charAt(i).sup() + formattedFormula
            }
          } else if (!isNaN(formula.charAt(i))) {
            formattedFormula = formula.charAt(i).sub() + formattedFormula
          } else {
            formattedFormula = formula.charAt(i) + formattedFormula
          }
        }
        return formattedFormula
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
