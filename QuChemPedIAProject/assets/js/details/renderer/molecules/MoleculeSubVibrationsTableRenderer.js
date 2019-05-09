import Renderer from "../Renderer";

/**
 * @external TableRenderer
 */

/**
 *
 */
export default class MoleculeSubVibrationsTableRenderer extends Renderer{

    /**
     *
     * @param {TableRenderer} tableRenderer
     */
    constructor(tableRenderer) {
        super();
        this._tableRenderer = tableRenderer;
    }

    /**
     * @typedef MoleculeFrenquencies
     * @property {Number[]} vibrational_int
     * @property {Number[]} vibrational_freq
     * @property {Number[]} vibrational_sym
     */

    /**
     *
     * @param freq
     * @param rootElement
     */
    render(freq, rootElement) {
        if (!freq.vibrational_int) return;

        const containerHtmlElement = document.createElement("div");
        containerHtmlElement.classList.add("container", "subVibrations");

        const row = document.createElement("div");
        row.classList.add("row");

        const tableColumn = document.createElement("div");
        tableColumn.classList.add("col-md-6","col-sm-6", "col-xs-6");

        this.renderSubVibrationTable(freq, tableColumn);


    }

    /**
     *
     * @param {MoleculeFrenquencies} freq
     * @param rootElement
     */
    renderSubVibrationTable(freq, rootElement) {
        const labelsDescriptions = [
            { headerInnerHtml : "Frequencies (cm<sup>-1</sup>)", key: "freq" },
            { headerInnerHtml: "Intensity (km/mol)", key: "intensity" },
            { headerInnerHtml: "Symmetry", key: "symmetry" }
        ];

        let tableData = [];

        // TODO ASK CONFIRMATION BECAUSE ITS FUCKING WEIRD TO NOT RENDER ANYTHING WHEN THERE IS BETWEEN 5 AND 19 VALUES
        // yes this is weird.
        if (freq.vibrational_int.length < 5) {
            tableData = freq.vibrational_int.map((value, index) => {
                return {
                    freq: freq.vibrational_freq[index],
                    intensity: freq.vibrational_int[index],
                    symmetry: freq.vibrational_sym[index],
                }
            });
        } else if (freq.vibrational_int.length > 20) {
            tableData = freq.vibrational_int.map((value, index) => {
                return {
                    freq: Math.round(freq.vibrational_freq[index]),
                    intensity: Math.round(freq.vibrational_int[index]),
                    symmetry: Math.round(freq.vibrational_sym[index]),
                }
            });
        }

        this._tableRenderer.render({labelsDescriptions, data: tableData, opt: {}}, rootElement);
    }
}