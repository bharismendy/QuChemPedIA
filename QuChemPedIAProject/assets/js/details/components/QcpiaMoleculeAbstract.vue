<template>
    <b-card
        title="Molecule"
    >
        <div class="container">
            <div class="row" v-if="molecule.iupac">
                <div class="col row">
                    <span class="font-weight-bold col">Iupac</span>
                    <qcpia-help-badge-link
                        class="col-1"
                        href="https://en.wikipedia.org/wiki/Union_internationale_de_chimie_pure_et_appliqu%C3%A9e"
                        tooltip-text="International Union of Pure and Applied Chemistry"
                        target="_blank" />
                </div>
                <div class="col">{{ molecule.iupac }}</div>
            </div>
            <!-- TOOD -->
        </div>
    </b-card>
</template>

<script>
  import QcpiaHelpBadgeLink from "./QcpiaHelpBadgeLink";
  export default {
      components: {QcpiaHelpBadgeLink},
      props: {
      molecule: {
        type: Object,
        required: true,
      }
    },
    name: "QcpiaMoleculeAbstract.vue"
  }
</script>

<style scoped>

</style>