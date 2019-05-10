<template>
  <b-card>
    <h5 slot="header">
      Molecule
    </h5>
    <div class="container">
      <div
        v-if="molecule.iupac"
        class="row"
      >
        <div class="col row">
          <span class="font-weight-bold mr-2">Iupac</span>
          <qcpia-help-badge-link
            href="https://en.wikipedia.org/wiki/Union_internationale_de_chimie_pure_et_appliqu%C3%A9e"
            tooltip-text="International Union of Pure and Applied Chemistry"
            target="_blank"
          />
        </div>
        <div
          class="col"
          data-testid="molecule_iupac"
        >
          {{ molecule.iupac }}
        </div>
      </div>
      <div
        v-if="molecule.inchi"
        class="row"
      >
        <div class="col">
          <span class="font-weight-bold mr-2">Inchi</span>
          <qcpia-help-badge-link
            href="https://en.wikipedia.org/wiki/International_Chemical_Identifier"
            tooltip-text="International Chemical Identifier"
            target="_blank"
          />
        </div>
        <div
          class="col"
          data-testid="molecule_inchi"
        >
          {{ molecule.inchi }}
        </div>
      </div>
      <div
        v-if="molecule.can"
        class="row"
      >
        <div class="col">
          <span class="font-weight-bold mr-2">Canonical SMILES</span>
          <qcpia-help-badge-link
            href="https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_Specification"
            tooltip-text=""
            target="_blank"
          />
        </div>
        <div
          class="col"
          data-testid="molecule_can"
        >
          {{ molecule.can }}
        </div>
      </div>
      <div
        v-if="molecule.monoisotopic_mass"
        class="row"
      >
        <div class="col">
          <span class="font-weight-bold">Monoisotopic mass</span>
        </div>
        <div
          class="col"
          data-testid="molecule_monoisotopic_mass"
        >
          {{ molecule.monoisotopic_mass }}
        </div>
      </div>
      <div
        v-if="molecule.formula"
        class="row"
      >
        <div class="col">
          <span class="font-weight-bold">Formula</span>
        </div>
        <div
          class="col"
          data-testid="molecule_formula"
          v-html="formattedFormula"
        />
      </div>
      <div
        v-if="molecule.charge !== undefined && molecule.charge !== null"
        class="row"
      >
        <div class="col">
          <span class="font-weight-bold">Charge</span>
        </div>
        <div
          class="col"
          data-testid="molecule_charge"
        >
          {{ molecule.charge }}
        </div>
      </div>
      <div
        v-if="molecule.multiplicity !== undefined && molecule.multiplicity !== null"
        class="row"
      >
        <div class="col">
          <span class="font-weight-bold">Spin Multiplicity</span>
        </div>
        <div
          class="col"
          data-testid="molecule_multiplicity"
        >
          {{ molecule.multiplicity }}
        </div>
      </div>
    </div>
  </b-card>
</template>

<script>
import QcpiaHelpBadgeLink from './QcpiaHelpBadgeLink.vue'

export default {
  name: 'QcpiaMoleculeAbstract',
  components: { QcpiaHelpBadgeLink },
  // data () {return {}}
  props: {
    molecule: {
      type: Object,
      required: true
    }
  },
  computed: {
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
    }
  }
}
</script>

<style scoped>

</style>
