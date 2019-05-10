<template>
  <div class="container">
    <QcpiaMolecule v-if="detailsLoaded && molecule"
                   :molecule="molecule"
                   :results="results"
                   :metadata="metadata"
    />
  </div>
</template>

<script>
  import QcpiaMolecule from "./QcpiaMolecule.vue";

  export default {
    components: {QcpiaMolecule},
    props: {
      id: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        detailsLoading: false,
        detailsLoaded: false,
        detailsLoadingError: null,
        molecule: null,
        metadata: null,
        results: null
      }
    },
    mounted () {
      // TODO load molecule
    },
    name: "QcpiaDetails"
  }
</script>