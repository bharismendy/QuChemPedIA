<template>
  <div>
    <section>
      <h5 class="border-bottom pb-1">
        Submissions
      </h5>
      <b-table
        :fields="submissionsTableFieds"
        :items="submissionTableItems"
        :per-page="submissionTablePagination.itemsPerPage"
        :current-page="submissionTablePagination.currentPage"
        borderless
        show-empty
      >
        <template
          slot="fileId"
          slot-scope="data"
        >
          <a :href="`details?id=${data.item.fileId}`"><i
            class="fa fa-external-link"
            aria-label="Open"
          /></a>
        </template>
      </b-table>
      <b-pagination
        v-if="displaySubmissionPagination"
        v-model="submissionTablePagination.currentPage"
        :total-rows="submissionTableItems.length"
        :per-page="submissionTablePagination.itemsPerPage"
        align="right"
        size="sm"
      />
    </section>
    <section>
      <h5 class="border-bottom pb-1">
        Siblings
      </h5>
      <div class="px-4">
        <qcpia-molecule-associated-calculations-sibling
          v-for="(sibling, index) in paginatedSiblingTableItems"
          :key="`${sibling.fileId}-${index}`"
          :sibling="sibling"
          class="py-2 mt-3"
        />
      </div>
      <b-pagination
        v-if="displaySiblingPagination"
        v-model="siblingsTablePagination.currentPage"
        :total-rows="siblingsTableItems.length"
        :per-page="siblingsTablePagination.itemsPerPage"
        align="right"
        size="sm"
      />
    </section>
  </div>
</template>

<script>
import AuthorRepository from '../../api/AuthorRepository'
import QcpiaMoleculeAssociatedCalculationsSibling from './QcpiaMoleculeAssociatedCalculationsSibling.vue'

export default {
  name: 'QcpiaMoleculeAssociatedCalculations',
  components: { QcpiaMoleculeAssociatedCalculationsSibling },
  props: {
    siblings: {
      // `Object[]`
      type: Array,
      required: true
    },
    metadata: {
      type: Object,
      required: true
    },
    authorRepository: {
      type: AuthorRepository,
      required: true
    }
  },
  data () {
    return {
      siblingsTableFields: [
        { key: 'jobType', label: 'Job Type' },
        { key: 'authorName', label: 'Author Name' },
        { key: 'fileId', label: '' }
      ],
      submissionsTableFieds: [
        { key: 'authorName', label: 'Author Name' },
        { key: 'fileId', label: '' }
      ],
      siblingsTablePagination: {
        itemsPerPage: 5,
        currentPage: 1
      },
      submissionTablePagination: {
        itemsPerPage: 5,
        currentPage: 1
      }

    }
  },
  computed: {
    siblingsTableItems () {
      return this.siblings.map((sibling) => {
        return {
          jobTypes: sibling.job ? sibling.job.join(', ') : 'Unknown',
          authorName: sibling.author ? sibling.author.name : 'N/A',
          fileId: sibling.id_log,
          basisSetName: sibling.basis_set_name ? (sibling.basis_set_name === 'Null' ? 'Unknown' : sibling.basis_set_name) : 'Unknown',
          'charge': sibling.charge !== null && sibling.charge !== undefined ? sibling.charge : 'Unknown',
          'endingEnergy': sibling.ending_energy || 'Unknown',
          'solvent': sibling.solvent || 'Unknown',
          'functionnal': sibling.functional || 'Unknown',
          'multiplicity': sibling.multiplicity || 'Unknown',
          'software': sibling.software || 'Unknown'
        }
      })
    },
    displaySiblingPagination () {
      return this.siblingsTableItems.length > this.siblingsTablePagination.itemsPerPage
    },
    paginatedSiblingTableItems () {
      const start = (this.siblingsTablePagination.currentPage - 1) * this.siblingsTablePagination.itemsPerPage
      const end = (this.siblingsTablePagination.currentPage) * this.siblingsTablePagination.itemsPerPage
      return this.siblingsTableItems.slice(start, end)
    },
    submissionTableItems () {
      return this.metadata.submissions.map((submission) => {
        return {
          authorName: submission.authorName ? submission.authorName : 'N/A',
          fileId: submission.id_log
        }
      })
    },
    displaySubmissionPagination () {
      return this.submissionTableItems.length > this.siblingsTablePagination.itemsPerPage
    }
  },
  watch: {
    siblings: {
      deep: true,
      handler () {
        this.loadSiblingsAuthors()
      }
    },
    'metadata.submissions': {
      deep: true,
      handler () {
        this.loadSubmissionsAuthors()
      }
    }
  },
  mounted () {
    this.loadSiblingsAuthors()
    this.loadSubmissionsAuthors()
  },
  methods: {
    loadSiblingsAuthors () {
      this.siblings.forEach((sibling) => {
        if (sibling.id_author) {
          this.authorRepository.findAuthorById(sibling.id_author)
            .then((author) => {
              this.$set(sibling, 'author', author)
            })
        }
      })
    },
    loadSubmissionsAuthors () {
      this.metadata.submissions.forEach((submissions) => {
        if (submissions.author) {
          this.authorRepository.findAuthorById(submissions.author)
            .then((author) => {
              this.$set(submissions, 'authorName', author.name)
            })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
