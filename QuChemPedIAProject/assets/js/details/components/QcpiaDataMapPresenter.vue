<template>
  <div>
    <div
      v-for="(element, index) in data"
      :key="index"
      class="row"
      data-testid="data-row"
    >
      <div
        class="col"
        :class="labelClasses"
        :data-testid="`data-label-${index}`"
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
        :data-testid="`data-value-${index}`"
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
