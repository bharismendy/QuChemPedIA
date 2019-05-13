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
      const data = response.data.data
      console.log(data)
      if (data.molecule) this.molecule = data.molecule
      if (data.metadata) this.metadata = data.metadata
      if (data.results) this.results = data.results
      if (data.comp_details) this.computationalDetails = data.comp_details
    }).catch(err => {
      this.detailsLoadingError = err
    }).then(() => {
      this.detailsLoaded = true
      this.detailsLoading = false
    })
  }
}
</script>
