<template>
  <canvas
    ref="canvas"
  />
</template>

<script>

export default {
  name: 'QcpiaMoleculeSmiles',

  props: {
    smiles: {
      type: String,
      required: true
    },
    canvasId: {
      type: String,
      required: false,
      default: 'smiles-canvas'
    }
  },
  computed: {
    width () {
      if (!this.$refs.canvas) return 500
      return this.$refs.canvas.width
    },

    options () {
      const size = this.width
      return {
        height: size,
        width: size,
        padding: 0
      }
    }
  },
  mounted () {
    if (window.SmilesDrawer) {
      // I tried to do it without that timeout. I got weird canvas rendering errors.
      // I don't know why, but it works with the timeout
      setTimeout(() => {
        console.log(this.options)
        let smilesDrawer = new window.SmilesDrawer.Drawer(this.options)
        window.SmilesDrawer.parse(this.smiles, (tree) => {
          // Draw to the canvas
          smilesDrawer.draw(tree, this.$refs.canvas, 'light', false)
        }, function (err) {
          console.error(err)
        })
      }, 50)
    } else {
      console.error('no smiles drawer')
    }
  }
}
</script>

<style scoped>

</style>
