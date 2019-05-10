<template>
  <div class="container">
    <qcpia-molecule
      v-if="detailsLoaded && molecule"
      :molecule="molecule"
      :results="results"
      :metadata="metadata"
      :computational-details="computationalDetails"
    />
  </div>
</template>

<script>
import QcpiaMolecule from './QcpiaMolecule.vue'
import axios from 'axios'
export default {
  name: 'QcpiaDetails',
  components: { QcpiaMolecule },
  props: {
    id: {
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
      computationalDetails: null
    }
  },
  mounted () {
    console.log('Coucou')
    this.detailsLoading = true
    axios.get('/access/details_json', {
      params: {
        id_file: this.id
      }
    }).then((response) => {
      if (response.data.molecule) this.molecule = response.data.molecule
      if (response.data.metadata) this.metadata = response.data.metadata
      if (response.data.results) this.results = response.data.results
      if (response.data.comp_details) this.computationalDetails = response.data.comp_details
    }).catch(err => {
      this.detailsLoadingError = err
    }).then(() => {
      this.detailsLoaded = true
      this.detailsLoading = false
    })
  }
}
</script>
