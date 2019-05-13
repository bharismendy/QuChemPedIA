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
