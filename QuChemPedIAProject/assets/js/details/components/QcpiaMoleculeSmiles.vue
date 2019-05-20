<template>
  <div>
    <transition name="fadeUp">
      <canvas
        v-show="drawingReady"
        ref="canvas"
        @click="openDialog"
      />
    </transition>

    <b-modal
      ref="modal"
      v-model="showDialog"
      static
      size="xl"
      scrollable
      hide-footer
    >
      <canvas
        ref="modalCanvas"
        style="width: 100%; height: 100%"
        class="mt-n5"
      />
    </b-modal>
  </div>
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
  data () {
    return {
      showDialog: false,
      drawingReady: false
    }
  },
  computed: {
    width () {
      if (!this.$refs.canvas) return 500
      return this.$refs.canvas.scrollWidth
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
      this.drawingReady = true
      // I tried to do it without that timeout. I got weird canvas rendering errors.
      // I don't know why, but it works with the timeout
      setTimeout(() => {
        let smilesDrawer = new window.SmilesDrawer.Drawer(this.options)
        window.SmilesDrawer.parse(this.smiles, (tree) => {
          // Draw to the canvas
          smilesDrawer.draw(tree, this.$refs.canvas, 'light', false)
        }, function (err) {
          console.error(err)
        })
      }, 50)
    } else {
      console.error('no smiles drawer') // Should never happen in production, check only for developpement if we change the django templates.
    }
  },
  methods: {
    openDialog () {
      this.showDialog = true
      setTimeout(() => {
        let size = 500
        if (this.$refs.modalCanvas) { size = this.$refs.modalCanvas.scrollWidth }
        // const size = this.$refs.modalCanvas.width
        // noinspection JSSuspiciousNameCombination
        let smilesDrawer = new window.SmilesDrawer.Drawer({
          height: size,
          width: size
        })
        window.SmilesDrawer.parse(this.smiles, (tree) => {
          // Draw to the canvas
          smilesDrawer.draw(tree, this.$refs.modalCanvas, 'light', false)
        }, function (err) {
          console.error(err)
        })
      }, 250)
    }
  }
}
</script>

<style scoped>

</style>
