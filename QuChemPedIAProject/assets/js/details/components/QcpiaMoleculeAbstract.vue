<template>
  <b-card
    title="Molecule"
  >
    <div class="container">
      <div
        v-if="molecule.iupac"
        class="row"
      >
        <div class="col row">
          <span class="font-weight-bold col">Iupac</span>
          <qcpia-help-badge-link
            class="col-1"
            href="https://en.wikipedia.org/wiki/Union_internationale_de_chimie_pure_et_appliqu%C3%A9e"
            tooltip-text="International Union of Pure and Applied Chemistry"
            target="_blank"
          />
        </div>
        <div class="col">
          {{ molecule.iupac }}
        </div>
      </div>
      <!-- TODO -->
    </div>
  </b-card>
</template>

<script>
import QcpiaHelpBadgeLink from './QcpiaHelpBadgeLink.vue'

export default {
  name: 'QcpiaMoleculeAbstract',
  components: { QcpiaHelpBadgeLink },
  props: {
    molecule: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
