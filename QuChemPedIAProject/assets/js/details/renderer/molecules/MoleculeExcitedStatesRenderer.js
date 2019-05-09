import Renderer from "../Renderer";

/**
 * @external TableRenderer
 */

export default class MoleculeExcitedStatesRenderer extends Renderer {

    /**
     *
     * @param {TableRenderer} tableRenderer
     */
    constructor(tableRenderer) {
        super();
        this._tableRenderer = tableRenderer;
    }

    render(excitedStates, rootElement) {

        const subCardHtmlElement = document.createElement("div");

        subCardHtmlElement.classList.add("container", "subCard");
        subCardHtmlElement.id = "ExcitedStates";

        const titleElement = document.createElement("h5");
        titleElement.classList.add("card-title");
        titleElement.innerText = "Excited states";

        subCardHtmlElement.appendChild(titleElement);

        if(excitedStates.et_energies) {

        }

        rootElement.appendChild(subCardHtmlElement);

        this._createExcitationTableHtmlElement(excitedStates, subCardHtmlElement);

        // TODO maybe : image ?
    }

    /**
     *
     * @param excitedStates
     * @param {HTMLElement} rootElement
     * @private
     */
    _createExcitationTableHtmlElement (excitedStates, rootElement) {
        const et_energies = excitedStates.et_energies;
        const inde = [];
        var N = 10;
        for (var i = 0; i < et_energies.length; i++){
            inde[i] = i + 1;
        }
        const et_sym = excitedStates.et_sym;
        const et_oscs = excitedStates.et_oscs;
        const et_rot = excitedStates.et_rot;

        const labelsDescriptions = [
            { headerInnerHtml: "Number", key: "number"},
            { headerInnerHtml: "Energy (cm<sup>-1</sup>)", key: "energyCm"},
            { headerInnerHtml: "Energy (nm)", key: "energyNm" },
            { headerInnerHtml: "Symmetry", key: "symmetry" },
            { headerInnerHtml: "Oscillator strength", key: "oscillatorStrength" },
            { headerInnerHtml: "Rotatory strength", key: "rotatoryStrength" }
        ];

        const tableData = et_energies.map((energy, i) => {
            return {
                number: inde[i],
                energyCm: Math.round(et_energies[i]),
                energyNm: Math.round(10000000 / et_energies[i]),
                symmetry: et_sym[i],
                oscillatorStrength: et_oscs[i],
                rotatoryStrength: et_rot[i] ? et_rot[i].toFixed(4) : "Unknown"
            }
        })

        this._tableRenderer.render({
            labelsDescriptions,
            data: tableData,
            opt: {}
        }, rootElement)

    }
}