<template>
  <div>
    <b-card class="mt-3">
      <h5 slot="header">
        Molecule
      </h5>
      <QcpiaMoleculeAbstract :molecule="molecule" />
    </b-card>
    <b-card class="mt-3">
      <h5 slot="header">
        Authorship
      </h5>
      <qcpia-molecule-authorship
        :metadata="metadata"
        :author-repository="authorRepository"
      />
    </b-card>
    <b-card class="mt-3">
      <h5 slot="header">
        Computational Details
      </h5>
      <qcpia-molecule-computational-details
        :computational-details="computationalDetails"
      />
    </b-card>
    <b-card class="mt-3">
      <h5 slot="header">
        Results
      </h5>
      <qcpia-molecule-results
        :molecule="molecule"
        :results="results"
        :computational-details="computationalDetails"
      />
    </b-card>
  </div>
</template>

<script>
import QcpiaMoleculeAbstract from './QcpiaMoleculeAbstract.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaMoleculeResults from './QcpiaMoleculeResults.vue'
import QcpiaMoleculeAuthorship from './QcpiaMoleculeAuthorship.vue'
import AuthorRepository from '../../api/AuthorRepository'

export default {
  name: 'QcpiaMolecule',
  components: { QcpiaMoleculeAuthorship, QcpiaMoleculeResults, QcpiaMoleculeComputationalDetails, QcpiaMoleculeAbstract },
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
    authorRepository: {
      type: AuthorRepository,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
