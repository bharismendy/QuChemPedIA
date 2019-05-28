<template>
  <div>
    <div
      v-if="metadata.log_file"
      class="row"
    >
      <div class="col text-muted">
        Original log file
      </div>
      <div class="col">
        <a :href="logFileLink">
          <i class="fa fa-download mr-1" />
          Download
        </a>
      </div>
    </div>
    <div
      v-if="metadata.id_user"
      class="row"
    >
      <div class="col text-muted">
        Primary Author
      </div>
      <div class="col">
        <template v-if="loadingAuthor">
          <i class="fas fa-spinner fa-spin" />
        </template>
        <template v-else>
          {{ author ? author.name : 'N/A' }}
        </template>
      </div>
    </div>
    <div
      v-if="metadata.affiliation"
      class="row"
    >
      <div class="col text-muted">
        Affiliation
      </div>
      <div class="col">
        {{ metadata.affiliation }}
      </div>
    </div>
  </div>
</template>

<script>
import AuthorRepository from '../../api/AuthorRepository'

export default {
  name: 'QcpiaMoleculeAuthorship',
  props: {
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
      loadingAuthor: false,
      author: null
    }
  },
  computed: {
    logFileLink () {
      const baseUrl = this.$root.baseUrl
      const dataDir = this.$root.dataDir
      return `${baseUrl}${dataDir}${this.metadata.log_file}`
    }
  },
  watch: {
    'metadata.id_user' () {
      this.loadAuthor()
    }
  },
  mounted () {
    this.loadAuthor()
  },
  methods: {
    loadAuthor () {
      this.author = null
      if (this.metadata.id_user) {
        this.loadingAuthor = true
        this.authorRepository.findAuthorById(this.metadata.id_user)
          .then((author) => {
            console.log({ author })
            this.$set(this, 'author', author)
          }).catch(() => {
            this.author = null
          }).then(() => { this.loadingAuthor = false })
      }
    }
  }
}
</script>

<style scoped>

</style>
