<template>
  <div>
    <QcpiaMoleculeAbstract :molecule="molecule" />
  </div>
</template>

<script>
  import QcpiaMoleculeAbstract from "./QcpiaMoleculeAbstract.vue";
  export default {
    props: {
      molecule: {
        type: Object,
        required: true,
      },
      metadata: {
        type: Object,
        required: true,
      },
      results: {
        type: Object,
        required: true
      }
    },
    name: "QcpiaMolecule",
    components: {QcpiaMoleculeAbstract}
  }
</script>

<style scoped>

</style>