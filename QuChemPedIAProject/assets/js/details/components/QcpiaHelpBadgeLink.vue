<template>
  <a
    v-b-tooltip.hover
    :href="href"
    :target="target"
    :title="tooltipText"
    class="badge badge-pill monBadge font-weight-bold text-primary"
  >
    ?
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
      // `_blank`
      default: '_blank'
    }
  }
}
</script>

<style scoped>

</style>
