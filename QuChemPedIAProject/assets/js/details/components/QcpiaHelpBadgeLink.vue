<template>
  <a :href="href" :target="target" v-b-tooltip.hover :title="tooltipText">
    <span class="badge badge-pill">?</span>
  </a>
</template>

<script>
  export default {
    props: {
      tooltipText: {
        type: String,
        required: true
      },
      href: {
        type: String,
        required: true
      },
      target: {
        type: String,
        required: false,
        default: "_blank"
      }
    },
    name: "QcpiaHelpBadgeLink"
  }
</script>

<style scoped>

</style>