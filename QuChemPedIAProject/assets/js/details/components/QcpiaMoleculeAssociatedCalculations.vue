<template>
  <b-table
    :items="tableItems"
    :fields="tableFields"
    borderless
  >
    <template
      slot="fileId"
      slot-scope="data"
    >
      <a :href="`details?id=${data.item.fileId}`"><i class="fa fa-file-text" /> </a>
    </template>
  </b-table>
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
    authorRepository: {
      type: AuthorRepository,
      required: true
    }
  },
  data () {
    return {
      tableFields: [
        { key: 'jobType', label: 'Job Type' },
        { key: 'authorName', label: 'Author Name' },
        { key: 'fileId', label: '' }
      ]
    }
  },
  computed: {
    tableItems () {
      return this.siblings.map((sibling) => {
        return {
          jobType: sibling.job_type,
          authorName: sibling.author ? sibling.author.name : 'N/A',
          fileId: sibling.id_ES
        }
      })
    }
  },
  watch: {
    siblings: {
      deep: true,
      handler () {
        this.loadAuthors()
      }
    }
  },
  mounted () {
    this.loadAuthors()
  },
  methods: {
    loadAuthors () {
      this.siblings.forEach((sibling) => {
        if (sibling.id_author) {
          this.authorRepository.findAuthorById(sibling.id_author)
            .then((author) => {
              this.$set(sibling, 'author', author)
            })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
