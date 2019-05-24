<template>
  <div>
    <div
      v-for="(element, index) in data"
      :key="index"
      class="row"
      :class="rowClasses"
      data-testid="data-row"
    >
      <template v-if="labelPosition === 'left'">
        <div
          class="col"
          :class="labelClasses"
          :data-testid="`data-label-${index}`"
        >
          <!-- Label slot -->
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
          <!-- Value slot -->
          <slot
            name="value"
            :element="element"
            :index="index"
          >
            <template
              v-if="element._rawHtml"
            >
              <span v-html="element.value" />
            </template>
            <template v-else>
              {{ element.value }}
            </template>
          </slot>
        </div>
      </template>
      <template v-else>
        <div class="col">
          <div
            :class="labelClasses"
            :data-testid="`data-label-${index}`"
          >
            <!-- Label slot -->
            <slot
              name="label"
              :element="element"
              :index="index"
            >
              {{ element.label }}
            </slot>
          </div>
          <div
            :class="valueClasses"
            :data-testid="`data-value-${index}`"
          >
            <!-- Value slot -->
            <slot
              name="value"
              :element="element"
              :index="index"
            >
              <template
                v-if="element._rawHtml"
                v-html="element.value"
              />
              <template v-else>
                {{ element.value }}
              </template>
            </slot>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QcpiaDataMapPresenter',
  props: {
    // An array of object with properties `label` and `value`
    data: {
      // `Object[]`
      type: Array,
      required: true
    },
    // Classes for the labels elements
    labelClasses: {
      // `String[]`
      type: Array,
      required: false,
      // `['font-weight-bold']`
      default () {
        return ['font-weight-bold']
      }
    },
    // Classes for the value element
    valueClasses: {
      // `String[]`
      type: Array,
      required: false,
      // `[]`
      default () {
        return []
      }
    },
    rowClasses: {
      type: Array,
      required: false,
      default () { return [] }
    },
    labelPosition: {
      // `top` / `left`
      type: String,
      required: false,
      // `left`
      default: 'left'
    }
  }
}
</script>

<style scoped>

</style>
