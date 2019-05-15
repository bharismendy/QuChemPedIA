/**
 *
 * @param {Object} object
 * @param {String|String[]} path
 */
export function valueFromPath (object, path) {
  if (typeof path === 'string') {
    path = path.split('.')
  }

  const last = path[path.length - 1]

  const lastObject = path.slice(0, path.length - 1).reduce((current, prop) => {
    if (current !== null && current !== undefined) {
      return current[prop]
    }
    return undefined
  }, object)
  if (lastObject !== null && lastObject !== undefined) {
    return lastObject[last]
  }
  return undefined
}

export function isObjectEmpty (obj) {
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) { return false }
  }
  return true
}

/**
 *
 * @param {Number} number
 * @param {Number|null} [fractionDigit]
 */
export function exponentialToHtmlString (number, fractionDigit = undefined) {
  const rawStr = `${number.toExponential(fractionDigit)}`

  const posE = rawStr.indexOf('e')

  const coeficient = rawStr.slice(0, posE)
  const exponent = rawStr.slice(posE + 1)

  if (coeficient === '1') {
    return `10<sup>${exponent}</sup>`
  }

  return `${coeficient}×10<sup>${exponent}</sup>`
}
