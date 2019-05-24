<template>
  <div>
    <h5 class="border-bottom pb-1">
      Submissions
    </h5>
    <b-table
      :fields="submissionsTableFieds"
      :items="submissionTableItems"
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

    <h5 class="border-bottom pb-1">
      Siblings
    </h5>
    <b-table
      :items="siblingsTableItems"
      :fields="siblingsTableFields"
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
  </div>
</template>

<script>
import AuthorRepository from '../../api/AuthorRepository'

export default {
  name: 'QcpiaMoleculeAssociatedCalculations',
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
      ]
    }
  },
  computed: {
    siblingsTableItems () {
      return this.siblings.map((sibling) => {
        return {
          jobType: sibling.job,
          authorName: sibling.author ? sibling.author.name : 'N/A',
          fileId: sibling.id_ES
        }
      })
    },
    submissionTableItems () {
      return this.metadata.submissions.map((submission) => {
        return {
          authorName: submission.authorName ? submission.authorName : 'N/A',
          fileId: submission.id_log
        }
      })
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
        if (submissions.id_author) {
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
