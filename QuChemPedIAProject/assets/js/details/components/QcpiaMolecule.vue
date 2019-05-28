<template>
  <div>
    <div
      class="text-muted font-italic text-right w-100"
      style="font-size: 0.75rem"
    >
      Molecule Id : {{ moleculeId }}
    </div>

    <template v-if="cardsDisplay">
      <div class="row">
        <div
          :class="{'col-lg-6': molecule.can}"
          class="col-12"
        >
          <b-card class="mt-4">
            <h5 slot="header">
              Molecule
            </h5>
            <qcpia-molecule-molecule :molecule="molecule" />
          </b-card>
        </div>
        <div class="col-12 col-lg-6">
          <qcpia-molecule-smiles :smiles="molecule.can" />
        </div>
      </div>
      <b-card class="mt-4">
        <h5 slot="header">
          Computational Details
        </h5>
        <qcpia-molecule-computational-details
          :computational-details="computationalDetails"
          :job-types="jobTypes"
        />
      </b-card>
      <b-card class="mt-4">
        <h5 slot="header">
          Authorship
        </h5>
        <qcpia-molecule-authorship
          :metadata="metadata"
          :author-repository="authorRepository"
        />
      </b-card>
      <b-card class="mt-4">
        <h5 slot="header">
          Associated Calculations
        </h5>
        <qcpia-molecule-associated-calculations
          :author-repository="authorRepository"
          :siblings="siblings"
          :metadata="metadata"
        />
      </b-card>
      <b-card class="mt-4">
        <h5 slot="header">
          Results
        </h5>
        <qcpia-molecule-results
          :molecule="molecule"
          :results="results"
          :computational-details="computationalDetails"
          :tabs-display="false"
        />
      </b-card>
      <b-card class="mt-4">
        <h5 slot="header">
          Visualisation
        </h5>
        <qcpia-molecule-viz-js-mol :metadata="metadata" />
      </b-card>
    </template>
    <b-card
      v-else
      no-body
      class="w-100 mb-4"
    >
      <b-tabs
        card
        fill
        class="w-100"
        @input="onTabChanged"
      >
        <b-tab
          title="Description"
          class="py-3"
        >
          <qcpia-molecule-abstract
            :molecule="molecule"
            :computational-details="computationalDetails"
            :author-repository="authorRepository"
            :metadata="metadata"
            :job-types="jobTypes"
          />
        </b-tab>
        <b-tab
          title="Results"
          class="py-3"
        >
          <qcpia-molecule-results
            :molecule="molecule"
            :results="results"
            :computational-details="computationalDetails"
          />
        </b-tab>
        <b-tab title="Associated Calculations">
          <qcpia-molecule-associated-calculations
            :siblings="siblings"
            :author-repository="authorRepository"
            :metadata="metadata"
          />
        </b-tab>
        <b-tab title="Visualisation">
          <qcpia-molecule-viz-js-mol :metadata="metadata" />
        </b-tab>
      </b-tabs>
    </b-card>
    <b-button-group
      style="position: fixed; bottom: 0; right: 0"
      class="m-2 bg-white opacity-50 hover-opacity-1"
    >
      <b-btn
        v-b-tooltip.hover
        title="Use tabs display"
        :variant="tabsDisplay ? 'primary' : 'outline-primary'"
        @click="display = 'tabs'"
      >
        <i
          class="fa fa-columns"
          aria-label="Use tab display"
        />
      </b-btn>
      <b-btn
        v-b-tooltip.hover
        title="Use cards display (best for printing)"
        :variant="cardsDisplay ? 'primary' : 'outline-primary'"
        @click="display = 'cards'"
      >
        <i
          class="fa fa-th-large"
          aria-label="Use card display"
        />
      </b-btn>
    </b-button-group>
  </div>
</template>

<script>
import QcpiaMoleculeAbstract from './QcpiaMoleculeAbstract.vue'
import QcpiaMoleculeResults from './QcpiaMoleculeResults.vue'
import QcpiaMoleculeAuthorship from './QcpiaMoleculeAuthorship.vue'
import AuthorRepository from '../../api/AuthorRepository'
import QcpiaMoleculeAssociatedCalculations from './QcpiaMoleculeAssociatedCalculations.vue'
import QcpiaMoleculeMolecule from './QcpiaMoleculeMolecule.vue'
import QcpiaMoleculeSmiles from './QcpiaMoleculeSmiles.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaMoleculeVizJsMol from './QcpiaMoleculeVizJsMol.vue'
import eBus from '../../event-bus'
export default {
  name: 'QcpiaMolecule',
  components: {
    QcpiaMoleculeVizJsMol,
    QcpiaMoleculeComputationalDetails,
    QcpiaMoleculeSmiles,
    QcpiaMoleculeMolecule,
    QcpiaMoleculeAssociatedCalculations,
    QcpiaMoleculeAuthorship,
    QcpiaMoleculeResults,
    QcpiaMoleculeAbstract
  },
  props: {
    molecule: {
      type: Object,
      required: true
    },
    jobTypes: {
      type: Array,
      required: true
    },
    metadata: {
      type: Object,
      required: true
    },
    results: {
      type: Object,
      required: true
    },
    computationalDetails: {
      type: Object,
      required: true
    },
    siblings: {
      type: Array,
      required: true
    },
    authorRepository: {
      type: AuthorRepository,
      required: true
    }
  },
  data () {
    return {
      display: 'tabs',
      tabs: ['molecule', 'results', 'authorship', 'associatedCalculations', 'viz']
    }
  },
  computed: {
    tabsDisplay () {
      return this.display === 'tabs'
    },
    cardsDisplay () {
      return this.display === 'cards'
    },
    moleculeId () {
      return this.$root.moleculeId
    }

  },
  methods: {
    onTabChanged (index) {
      eBus.$emit(eBus.signals.tabs.SWITCH, { name: this.tabs[index], data: { molecule: this.molecule, metadata: this.metadata } })
    }
  }
}
</script>

<style scoped>

</style>
