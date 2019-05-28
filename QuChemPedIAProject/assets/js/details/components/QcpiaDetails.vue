<template>
  <div>
    <transition name="fade">
      <qcpia-molecule
        v-if="detailsLoaded && molecule"
        :molecule="molecule"
        :results="results"
        :metadata="metadata"
        :computational-details="computationalDetails"
        :siblings="siblings"
        :author-repository="authorRepository"
        :job-types="jobTypes"
      />
    </transition>
    <b-spinner
      v-if="detailsLoading"
      label="Loading..."
      variant="accent"
      style="width: 5rem; height: 5rem; position: fixed; top: 0; left: 0; bottom: 0; right: 0; margin: auto;"
    />
    <qcpia-details404 v-if="detailsLoadingError" />
    <qcpia-notification-stack

      style="position: fixed; bottom: 0; right:0; max-width: 300px; "
    />
  </div>
</template>

<script>

import QcpiaMolecule from './QcpiaMolecule.vue'
import axios from 'axios'
import AuthorRepository from '../../api/AuthorRepository'
import QcpiaNotificationStack from '../../components/QcpiaNotificationStack.vue'
import eBus from '../../event-bus'
import QcpiaDetails404 from './QcpiaDetails404.vue'
// import Mock from '../mock'
// Entry component for the detail page
export default {
  name: 'QcpiaDetails',
  components: { QcpiaDetails404, QcpiaNotificationStack, QcpiaMolecule },
  props: {
    id: {
      type: String,
      required: true
    },
    baseUrl: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      detailsLoading: false,
      detailsLoaded: false,
      detailsLoadingError: null,
      molecule: null,
      metadata: null,
      results: null,
      siblings: [],
      computationalDetails: null,
      authorRepository: new AuthorRepository(this.baseUrl),
      jobTypes: null
    }
  },
  mounted () {
    this.detailsLoading = true
    axios.get('/access/details_json', {
      params: {
        id_file: this.id
      }
    }).then((response) => {
      const data = response.data.data
      if (response.data.job_type) this.jobTypes = response.data.job_type
      if (data.molecule) this.molecule = data.molecule
      if (data.metadata) this.metadata = data.metadata
      if (data.results) this.results = data.results
      if (response.data.siblings) this.siblings = response.data.siblings
      if (data.comp_details) this.computationalDetails = data.comp_details
      // eBus.$emit(eBus.signals.notify.SUCCESS, { message: 'Molecule loaded' })
      this.detailsLoaded = true
    }).catch(err => {
      this.detailsLoadingError = err
      eBus.$emit(eBus.signals.notify.ERROR, { message: 'Failed to load molecule\n' + err })
    }).then(() => {
      this.detailsLoading = false
    })
  }
}
</script>
