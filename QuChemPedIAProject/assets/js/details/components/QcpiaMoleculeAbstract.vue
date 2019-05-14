<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-5 col-md-12">
        <qcpia-molecule-smiles
          v-if="molecule.can"
          :smiles="molecule.can"
        />
      </div>
      <div class="col-lg-7 col-md-12">
        <div class="row">
          <div
            class="col h3"
            data-testid="molecule_formula"
            v-html="formattedFormula"
          />
        </div>
        <div class="row">
          <div class="col font-weight-bold">
            Charge
          </div>
          <div
            class="col"
            data-testid="molecule_charge"
          >
            {{ molecule.charge }}
          </div>
        </div>
        <div class="row">
          <div class="col font-weight-bold">
            Spin Multiplicity
          </div>
          <div
            class="col"
            data-testid="molecule_multiplicity"
          >
            {{ molecule.multiplicity }}
          </div>
        </div>

        <div
          v-if="molecule.iupac"
          class="row mt-1"
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
          class="row mt-1"
        >
          <div class="col-4">
            <span class="font-weight-bold mr-2">Inchi</span>
            <qcpia-help-badge-link
              href="https://en.wikipedia.org/wiki/International_Chemical_Identifier"
              tooltip-text="International Chemical Identifier"
              target="_blank"
            />
          </div>
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
            v-b-tooltip.hover
            class="col-1 badge-pill badge badge-primary px-1 text-center"
            title="Copy"
            @click="copyInchi"
          >
            <i class="fa fa-copy" />
          </div>
          <input
            ref="inchiInput"
            type="hidden"
            :value="molecule.inchi.slice(6)"
          >
        </div>
        <div
          v-if="molecule.can"
          class="row mt-1"
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
            v-b-tooltip.hover
            class="col"
            data-testid="molecule_can"
            style="text-overflow: ellipsis;  white-space: nowrap;overflow: hidden;"
            :title="molecule.can"
          >
            {{ molecule.can }}
            <input
              ref="canInput"
              type="hidden"
              :value="molecule.can"
            >
          </div>
          <div
            v-b-tooltip.hover
            class="col-1 badge-pill badge badge-primary px-1 text-center"
            title="Copy"
            @click="copyCan"
          >
            <i class="fa fa-copy" />
          </div>
        </div>
        <div
          v-if="molecule.monoisotopic_mass"
          class="row mt-1"
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
      </div>
    </div>
  </div>
</template>

<script>
import QcpiaHelpBadgeLink from './QcpiaHelpBadgeLink.vue'
import QcpiaMoleculeSmiles from './QcpiaMoleculeSmiles.vue'

export default {
  name: 'QcpiaMoleculeAbstract',
  components: { QcpiaHelpBadgeLink, QcpiaMoleculeSmiles },
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
  },
  methods: {
    copyInput (ref) {
      const input = this.$refs[ref]
      input.setAttribute('type', 'text')
      input.select()

      try {
        document.execCommand('copy')
      } catch (err) {
        console.error(err)
      }

      /* unselect the range */
      input.setAttribute('type', 'hidden')
      window.getSelection().removeAllRanges()
    },
    copyInchi () {
      this.copyInput('inchiInput')
    },
    copyCan () {
      this.copyInput('canInput')
    }
  }
}
</script>

<style scoped>

</style>
