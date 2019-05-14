<template>
  <b-card
    no-body
    class="w-100"
  >
    <b-tabs card>
      <b-tab
        title="Molecule"
        class="py-3"
      >
        <qcpia-molecule-abstract :molecule="molecule" />
      </b-tab>
      <b-tab
        title="Authorship"
        class="py-3"
      >
        <qcpia-molecule-authorship
          :metadata="metadata"
          :author-repository="authorRepository"
        />
      </b-tab>
      <b-tab title="Associated Calculations">
        <qcpia-molecule-associated-calculations
          :siblings="siblings"
          :author-repository="authorRepository"
        />
      </b-tab>
      <b-tab
        title="Computational Details"
        class="py-3"
      >
        <qcpia-molecule-computational-details
          :computational-details="computationalDetails"
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
    </b-tabs>
  </b-card>
</template>

<script>
import QcpiaMoleculeAbstract from './QcpiaMoleculeAbstract.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaMoleculeResults from './QcpiaMoleculeResults.vue'
import QcpiaMoleculeAuthorship from './QcpiaMoleculeAuthorship.vue'
import AuthorRepository from '../../api/AuthorRepository'
import QcpiaMoleculeAssociatedCalculations from './QcpiaMoleculeAssociatedCalculations.vue'

export default {
  name: 'QcpiaMolecule',
  components: {
    QcpiaMoleculeAssociatedCalculations,
    QcpiaMoleculeAuthorship,
    QcpiaMoleculeResults,
    QcpiaMoleculeComputationalDetails,
    QcpiaMoleculeAbstract
  },
  props: {
    molecule: {
      type: Object,
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
  }
}
</script>

<style scoped>

</style>
