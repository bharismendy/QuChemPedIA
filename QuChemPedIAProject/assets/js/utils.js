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

export function moleculeFormulaToHtml (formula, charge) {
  let formattedFormula = ''
  for (let i = formula.length - 1; i >= 0; i--) {
    if (i === formula.length - 1 && charge !== 0) {
      if (charge > 1 || charge < -1) {
        formattedFormula = formula.charAt(i - 1).sup() + formula.charAt(i).sup() + formattedFormula
        i--
      } else {
        formattedFormula = formula.charAt(i).sup() + formattedFormula
      }
    } else if (!isNaN(formula.charAt(i))) {
      formattedFormula = formula.charAt(i).sub() + formattedFormula
    } else {
      formattedFormula = formula.charAt(i) + formattedFormula
    }
  }
  return formattedFormula
}
