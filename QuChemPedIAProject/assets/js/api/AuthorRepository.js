import axios from 'axios'

export default class AuthorsRepository {
  /**
   * @param {String} baseUrl
   */
  constructor (baseUrl) {
    this._baseUrl = baseUrl.charAt(baseUrl.length - 1) === '/' ? baseUrl : baseUrl + '/' // Make sure the baseUrl end with '/'

    this._authorRequestsPromiseMap = new Map()
  }

  /**
   *
   * @param {Number} id
   * @returns {Promise}
   */
  findAuthorById (id) {
    if (this._authorRequestsPromiseMap.has(id)) {
      return this._authorRequestsPromiseMap.get(id)
    }

    const promise = axios.get(`${this._baseUrl}access/details_author?id_author=${id}`)
      .then((response) => {
        const results = response.data
        if (results !== undefined && results !== null) {
          return {
            name: results.name,
            id: id
          }
        } else {
          throw new Error('Server returned unreadable response')
        }
      }).catch((err) => {
        this._authorRequestsPromiseMap.delete(id)
        throw err
      })

    this._authorRequestsPromiseMap.set(id, promise)

    return promise
  }

  clearCache () {
    this._authorRequestsPromiseMap.clear()
  }
}
