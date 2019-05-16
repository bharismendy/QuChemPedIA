<template>
  <div
    v-b-tooltip.hover
    class="copy-button copy-button-primary"
    :title="tooltipText"
    @click="copyTextToClipboard"
  >
    <slot>
      <i :class="icon" />
    </slot>
    <input
      ref="textInput"
      :value="text"
      type="hidden"
    >
  </div>
</template>

<script>
export default {
  name: 'QcpiaCopyTextButton',
  props: {
    text: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: false,
      default: 'fa fa-copy'
    },
    tooltipText: {
      type: String,
      required: false,
      default: null
    }
  },
  computed: {
  },
  methods: {
    copyTextToClipboard () {
      const input = this.$refs.textInput

      input.setAttribute('type', 'text')
      input.select()

      try {
        document.execCommand('copy')
        this.$emit('copied')
      } catch (err) {
        this.$emit('copy-error')
        console.error(err)
      }

      /* unselect the range */
      input.setAttribute('type', 'hidden')
      window.getSelection().removeAllRanges()
    }
  }
}
</script>

<style scoped>

</style>
