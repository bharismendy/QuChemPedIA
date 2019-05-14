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
    },
    options: {
      type: Object,
      required: false,
      default () {
        return {
          atomVisualization: 'none'
        }
      }
    }
  },
  mounted () {
    if (window.SmilesDrawer) {
      // I tried to do it without that timeout. I got weird canvas rendering errors.
      // I don't know why, but it works with the timeout
      setTimeout(() => {
        let smilesDrawer = new window.SmilesDrawer.Drawer({})
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
