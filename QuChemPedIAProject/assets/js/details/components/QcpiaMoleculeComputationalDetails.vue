<template>
  <b-card>
    <h5 slot="header">
      Computational details
    </h5>

    <QcpiaDataMapPresenter
      data-testid="computationalDetailsTable"
      :data="tableData"
      :label-classes="tableLabelClasses"
    />
  </b-card>
</template>

<script>
import QcpiaDataMapPresenter from './QcpiaDataMapPresenter.vue'
import { valueFromPath } from '../../utils'

export default {
  name: 'QcpiaMoleculeComputationalDetails',
  components: { QcpiaDataMapPresenter },
  props: {
    computationalDetails: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      tableLabelClasses: ['font-weight-bold'],

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
                  value: Number.parseFloat(targets[0]).toExponential() //TODO format to HTML
                },
                {
                  label: 'Requested SCF convergence on MAX density',
                  value: Number.parseFloat(targets[1]).toExponential() //TODO format to HTML
                },
                {
                  label: 'Requested SCF convergence on energy',
                  value: Number.parseFloat(targets[2]).toExponential() //TODO format to HTML
                }
              ]
            }
          }
        },
        // TODO SCF_TARGETS
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
      console.log(this.computationalDetails)
      return this.tableDataDef.reduce((acc, current) => {
        let value = valueFromPath(this.computationalDetails, current.path)
        if (value === undefined) { return acc }

        if (current.hasOwnProperty('handler')) {
          Array.prototype.push.apply(acc, current.handler(value))
        } else {
          if (current.hasOwnProperty('formatter')) {
            value = current.formatter(value)
          }
          acc.push({
            label: current.label,
            value
          })
        }
        return acc
      }, [])
    }
  }
}
</script>

<style scoped>

</style>
