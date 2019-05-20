<template>
  <QcpiaDataMapPresenter
    data-testid="computationalDetailsTable"
    :data="tableData"
    :label-classes="tableLabelClasses"
    :value-classes="tableValueClasses"
    :row-classes="tableRowClasses"
  />
</template>

<script>
import { exponentialToHtmlString } from '../../utils'
import QcpiaDataMapPresenter from './QcpiaDataMapPresenter.vue'
import tableDataMapHelper from '../mixins/tableDataMapHelpers'
export default {
  name: 'QcpiaMoleculeComputationalDetails',
  components: { QcpiaDataMapPresenter },
  mixins: [tableDataMapHelper],
  props: {
    computationalDetails: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      tableLabelClasses: ['text-muted', 'col-auto'],
      tableValueClasses: ['col-auto'],
      tableRowClasses: ['mt-1 justify-content-between'],
      tableDataDef: [
        {
          path: 'general.package',
          label: 'Software',
          formatter: () => {
            const software = this.computationalDetails.general.package
            const softwareVersionStr = this.computationalDetails.general.package_version ? ' ( ' + this.computationalDetails.general.package_version + ' )' : ''
            return `${software}${softwareVersionStr}`
          }
        },
        {
          path: 'general.last_theory',
          label: 'Computational method'
        },
        {
          path: 'general.functional',
          label: 'Functional'
        },
        {
          path: 'general.basis_set_name',
          label: 'Basis Set Name'
        },
        {
          path: 'general.basis_set_size',
          label: 'Number of basis set functions'
        },
        {
          path: 'general.is_closed_shell',
          label: 'Closed shell calculation'
        },
        {
          path: 'general.integration_grid',
          label: 'Integration grid'
        },
        {
          path: 'general.solvent',
          label: 'Solvent'
        },
        {
          path: 'general.scf_targets',
          handler: (value) => {
            if (value.length > 0) {
              const targets = value[value.length - 1]
              return [
                {
                  label: 'Requested SCF convergence on RMS density',
                  _rawHtml: true,
                  value: exponentialToHtmlString(Number.parseFloat(targets[0]))
                },
                {
                  label: 'Requested SCF convergence on MAX density',
                  _rawHtml: true,
                  value: exponentialToHtmlString(Number.parseFloat(targets[1])) // TODO format to HTML
                },
                {
                  label: 'Requested SCF convergence on energy',
                  _rawHtml: true,
                  value: exponentialToHtmlString(Number.parseFloat(targets[2])) // TODO format to HTML
                }
              ]
            }
          }
        },
        {
          path: 'freq.temperature',
          label: 'Temperature',
          formatter (value) {
            return `${value} K`
          }
        },
        {
          path: 'freq.anharmonicity',
          label: 'Anharmonic effects'
        },
        {
          path: 'excited_states.nb_et_states',
          label: 'Number of excited states'
        }
      ]
    }
  },
  computed: {
    tableData () {
      return this.buildTableData(this.tableDataDef, this.computationalDetails)
    }
  }
}
</script>

<style scoped>

</style>
