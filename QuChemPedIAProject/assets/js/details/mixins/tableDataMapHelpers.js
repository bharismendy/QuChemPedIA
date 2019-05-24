import { valueFromPath } from '../../utils'

export default {
  methods: {
    buildTableData (dataDef, baseData) {
      return dataDef.reduce((acc, current) => {
        let value = valueFromPath(baseData, current.path)
        if (value === undefined) { return acc }

        if (current.hasOwnProperty('handler')) {
          Array.prototype.push.apply(acc, current.handler(value))
        } else {
          if (current.hasOwnProperty('formatter')) {
            value = current.formatter(value)
          }
          acc.push({
            label: current.label,
            value,
            _rawHtml: current._rawHtml || false
          })
        }
        return acc
      }, [])
    }
  }
}
