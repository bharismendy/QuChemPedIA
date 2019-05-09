import Renderer from "../Renderer";

const DATA_LABELS_DEF =     [
                    {"label": "Sum of electronic and zero-point energy", key: "zero_point_energy"},
            {"label": "Sum of electronic and thermal ", key: "electronic_thermal_energy"},
            {"label": "Entropy", key: "entropy"},
            {"label": "Enthalpy", key: "enthalpy"},
            {"label": "Gibbs free energy", key: "free_energy"},

        ];


/**
 * @external TableRenderer
 */

export default class MoleculeThermochemistryRenderer extends Renderer {


    /**
     *
     * @param {TableRenderer} tableRenderer
     */
    constructor(tableRenderer) {
        super();
        this._tableRenderer = tableRenderer;
    }

    /**
     * @typedef ResultsFrequencies
     * @property [zero_point_energy]
     * @property [electronic_thermal_energy]
     * @property [entropy]
     * @property [enthalpy]
     * @property [free_energy]
     */

    /**
     *
     * @param {ResultsFrequencies} resultsFreq
     * @param {HTMLElement} rootElement
     */
    render(resultsFreq, rootElement) {
        const subCardContainer = document.createElement("div");
        subCardContainer.classList.add("container", "subWavefunction", "subCard")
        subCardContainer.id = "Thermochemistry";

        const textValueReference = document.createElement("span");
        textValueReference.innerText = "All values was calculated at 298.150000 K in atomic units."
        textValueReference.classList.add("font-italic");

        subCardContainer.appendChild(textValueReference);

        const labelsDescriptions = [
            {
                headerInnerHtml: "",
                key: "label",
            },
            {
                headerInnerHtml: "",
                key: "value"
            }
        ];

        const tableData = DATA_LABELS_DEF.reduce((acc, cur) => {
            if (resultsFreq.hasOwnProperty(cur.key)) {
                acc.push({
                    label: cur.label,
                    value: resultsFreq[cur.key]
                });
            }
            return acc;
        }, []);

        this._tableRenderer.render({labelsDescriptions, data: tableData, opt: {headers: false}}, subCardContainer);

        rootElement.appendChild(subCardContainer);
    }
}