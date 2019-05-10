<template>
  <div>
    <div
      v-for="(element, index) in data"
      :key="index"
      class="row"
    >
      <div
        class="col"
        :class="labelClasses"
      >
        <slot
          name="label"
          :element="element"
          :index="index"
        >
          {{ element.label }}
        </slot>
      </div>
      <div
        class="col"
        :class="valueClasses"
      >
        <slot
          name="value"
          :element="element"
          :index="index"
        >
          {{ element.value }}
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QcpiaDataMapPresenter',
  props: {
    data: {
      // `Object[]`
      type: Array,
      required: true
    },
    labelClasses: {
      // `String[]`
      type: Array,
      required: false,
      // `['font-weight-bold']`
      default () {
        return ['font-weight-bold']
      }
    },
    valueClasses: {
      // `String[]`
      type: Array,
      required: false,
      // `[]`
      default () {
        return []
      }
    }
  }
}
</script>

<style scoped>

</style>
