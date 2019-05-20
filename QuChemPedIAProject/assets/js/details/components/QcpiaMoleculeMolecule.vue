<template>
  <div>
    <div
      v-if="!isHidden('formula')"
      class="row mt-1"
    >
      <div class="col text-muted">
        Formula
      </div>
      <div
        class="col"
        v-html="formattedFormula"
      />
    </div>
    <div
      v-if="!isHidden('charge')"
      class="row mt-1"
    >
      <div class="col text-muted">
        Charge
      </div>
      <div class="col">
        {{ molecule.charge }}
      </div>
    </div>
    <div
      v-if="!isHidden('multiplicity')"
      class="row  mt-1"
    >
      <div class="col text-muted">
        Spin multiplicity
      </div>
      <div class="col">
        {{ molecule.multiplicity }}
      </div>
    </div>
    <div
      v-if="molecule.monoisotopic_mass && !isHidden('monoisotopic_mass')"
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
      v-if="molecule.iupac && !isHidden('iupac')"
      class="row mt-1"
    >
      <div class="col row">
        <div class="row align-items-center">
          <span class="col text-muted">Iupac</span>
          <qcpia-help-badge-link
            class="ml-2"
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
      v-if="molecule.inchi && !isHidden('inchi')"
      class="row mt-1"
    >
      <div class="col">
        <div class="row align-items-center">
          <span class="col text-muted">Inchi
            <qcpia-help-badge-link
              class="ml-2"
              href="https://en.wikipedia.org/wiki/International_Chemical_Identifier"
              tooltip-text="International Chemical Identifier"
              target="_blank"
            /></span>
        </div>
        <div class="row align-items-center">
          <div
            v-b-tooltip.hover
            class="col"
            data-testid="molecule_inchi"
            style="text-overflow: ellipsis;  white-space: nowrap;overflow: hidden;"
            :title="molecule.inchi.slice(6)"
          >
            {{ molecule.inchi.slice(6) }}
          </div>
          <div
            style="width: 2.5rem"
          >
            <qcpia-copy-text-button
              :text="molecule.inchi.slice(6)"
              tooltip-text="Copy"
              size="sm"
              variant="outline-primary"
              class="p-1 w-100 text-center"
              @copied="notifyCopy"
            />
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="molecule.can && !isHidden('can')"
      class="row mt-1"
    >
      <div class="col">
        <div class="row align-items-center">
          <span class="col text-muted">Canonical SMILES
            <qcpia-help-badge-link
              href="https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_Specification"
              tooltip-text="Simplified Molecular Input Line Entry Specification"
              target="_blank"
              class="ml-2"
            />
          </span>
        </div>
        <div class="row align-items-center">
          <div
            v-b-tooltip.hover
            class="col"
            data-testid="molecule_can"
            style="text-overflow: ellipsis;  white-space: nowrap;overflow: hidden;"
            :title="molecule.can"
          >
            {{ molecule.can }}
          </div>
          <div style="width: 2.5rem">
            <qcpia-copy-text-button
              :text="molecule.can"
              tooltip-text="Copy to clipboard"
              class="p-1 w-100 text-center"
              variant="outline-primary"
              size="sm"
              @copied="notifyCopy"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QcpiaCopyTextButton from './QcpiaCopyTextButton.vue'
import QcpiaHelpBadgeLink from './QcpiaHelpBadgeLink.vue'
import eBus from '../../event-bus'
import { moleculeFormulaToHtml } from '../../utils'

export default {
  name: 'QcpiaMoleculeMolecule',
  components: {
    QcpiaCopyTextButton,
    QcpiaHelpBadgeLink
  },
  props: {
    molecule: {
      type: Object,
      required: true
    },
    hiddenProps: {
      type: Array,
      required: false,
      default () {
        return []
      }
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
    }
  },

  methods: {
    notifyCopy () {
      eBus.$emit(eBus.signals.notify.SUCCESS, { message: 'Copied to clipboard' })
    },
    isHidden (props) {
      return this.hiddenProps.indexOf(props) !== -1
    }
  }
}
</script>

<style scoped>

</style>
