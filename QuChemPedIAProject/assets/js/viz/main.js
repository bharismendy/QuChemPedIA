
window.$.urlParam = function (name) { // fonction qui permet de récupérer l'url
  var results = new RegExp('[?&]' + name + '=([^&#]*)').exec(window.location.href)
  return results[1] || 0
}

function jmolInitViz (fileUrl, baseUrl) {
  const size = Math.min(document.querySelector('#apphere').clientWidth, 500)
  console.log({ size })
  const Info = {
    use: 'HTML5',
    width: size,
    height: size,
    debug: false,
    color: '0xC0C0C0',
    j2sPath: `${baseUrl}/common_qcpia/static/js/jsmol/j2s`,
    isSigned: 'true',
    disableJ2SLoadMonitor: true,
    disableInitialConsole: true,
    addSelectionOptions: false,
    serverURL: 'https://chemapps.stolaf.edu/jmol/jsmol/php/jsmol.php',
    // readyFunction: setOptions,
    script: `set zoomLarge falase; load ${fileUrl}`
  }

  console.log(Info)

  window.Jmol._document = null
  window.$('#apphere').html(window.Jmol.getAppletHtml('jmolApplet0', Info))
}

window.$(document).ready(() => {
  setTimeout(() => {
    const vizContainer = document.querySelector('#vizContainer')

    const logFile = window.$.urlParam('log_file')

    const dataDir = vizContainer.dataset.dataDir
    const baseUrl = vizContainer.dataset.baseUrl

    const fileUrl = `${baseUrl}${dataDir}${logFile}`
    console.log({ logFile, dataDir, fileUrl })
    jmolInitViz(fileUrl, baseUrl)
  }, 2000)
})
