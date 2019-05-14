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
        <div class="row">
          <div class="col-lg-6 col-md-12">
            <qcpia-molecule-smiles
              v-if="molecule.can"
              :smiles="molecule.can"
            />
          </div>
          <div class="col-lg-6 col-md-12">
            <qcpia-molecule-abstract :molecule="molecule" />
          </div>
        </div>
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
    <!--    <b-card class="mt-3">
      <h5 slot="header">
        Molecule
      </h5>
      <qcpia-molecule-abstract :molecule="molecule"/>
      <qcpia-molecule-smiles
          v-if="molecule.can"
          :smiles="molecule.can"
      />
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
        Associated Calculation
      </h5>
      <qcpia-molecule-associated-calculations
          :siblings="siblings"
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
    </b-card>-->
  </b-card>
</template>

<script>
import QcpiaMoleculeAbstract from './QcpiaMoleculeAbstract.vue'
import QcpiaMoleculeComputationalDetails from './QcpiaMoleculeComputationalDetails.vue'
import QcpiaMoleculeResults from './QcpiaMoleculeResults.vue'
import QcpiaMoleculeAuthorship from './QcpiaMoleculeAuthorship.vue'
import AuthorRepository from '../../api/AuthorRepository'
import QcpiaMoleculeAssociatedCalculations from './QcpiaMoleculeAssociatedCalculations.vue'
import QcpiaMoleculeSmiles from './QcpiaMoleculeSmiles.vue'

export default {
  name: 'QcpiaMolecule',
  components: {
    QcpiaMoleculeSmiles,
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
