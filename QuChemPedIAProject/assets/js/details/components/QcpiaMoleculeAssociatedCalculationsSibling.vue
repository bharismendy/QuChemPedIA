<template>
  <div
    class="row"
  >
    <div class="col">
      <div class="row">
        <div class="text-primary col">
          Job Types: <span class="font-weight-bold">{{ sibling.jobTypes }}</span>
        </div>
        <div class="text-primary col">
          Author: <span class="font-weight-bold">{{ sibling.authorName }}</span>
        </div>
        <div class="col text-primary">
          Software: <span class="font-weight-bold">{{ sibling.software }}</span>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div class="text-muted">
            Basis Set Name
          </div>
          <div>{{ sibling.basisSetName }}</div>
        </div>
        <div class="col">
          <div class="text-muted">
            Series
          </div>
          <div>{{ sibling.functionnal }}</div>
        </div>
        <div class="col">
          <div class="text-muted">
            Solvent
          </div>
          <div>
            {{ sibling.solvent }}
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div class="text-muted">
            Ending Energie
          </div>
          <div>{{ sibling.endingEnergy }}</div>
        </div>
        <div class="col">
          <div class="text-muted">
            Charge
          </div>
          <div>{{ sibling.charge }}</div>
        </div>
        <div class="col">
          <div class="text-muted">
            Multiplicity
          </div>
          <div>{{ sibling.multiplicity }}</div>
        </div>
      </div>
    </div>
    <div class="col-2">
      <b-btn
        :href="`details?id=${sibling.fileId}`"
        variant="outline-primary"
      >
        <i
          class="fa fa-external-link"
          aria-label="Open"
        />
      </b-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QcpiaMoleculeAssociatedCalculationsSiblingVue',
  props: {
    sibling: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
