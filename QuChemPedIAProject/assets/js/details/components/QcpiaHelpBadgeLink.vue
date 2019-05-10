<template>
  <a
    v-b-tooltip.hover
    :href="href"
    :target="target"
    :title="tooltipText"
  >
    <span class="badge badge-pill">?</span>
  </a>
</template>

<script>
export default {
  name: 'QcpiaHelpBadgeLink',
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
      default: '_blank'
    }
  }
}
</script>

<style scoped>

</style>
