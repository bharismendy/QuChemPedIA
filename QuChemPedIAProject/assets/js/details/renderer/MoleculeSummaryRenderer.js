import CardRenderer from "./CardRenderer";

export default class MoleculeSummaryRenderer{

    /**
     * @param {CardRenderer} cardRenderer
     */
    constructor(cardRenderer) {
        this._cardRenderer = cardRenderer;
        // super((data, rootElement) => this._renderHeader(data, rootElement), (data, rootElement) => this._renderBody(data, rootElement))
    }

    /**
     * @typedef Molecule
     * @property {Number} [multiplicity]
     * @property {Number} [charge]
     * @property {String} [formula]
     * @property {Number} [monoisotopic_mass]
     * @property {String} [inchi]
     * @property {String} [smi]
     * @property {Number} [nb_atoms]
     * @property {String} [can]
     * @property {String} [iupac]
     */

    /**
     *
     * @param {Molecule} data
     * @param {HTMLElement} rootElement
     */
    render(data, rootElement) {
        this._cardRenderer.render({
            headerRenderCallback: this._renderHeader,
            bodyRenderCallback: this._renderBody,
            data
        },
        rootElement)
    }

    // noinspection JSMethodCanBeStatic
    _renderHeader(data, headerElement) {
        headerElement.innerHTML = "<h5>Molecule</h5>"
    }

    /**
     * @param {Molecule} molecule
     * @param {HTMLElement} container
     * @private
     */
    _renderBody(molecule, container) {
        if (molecule.iupac) {
            const ipuacRow = this._createDataRow(
                "Iupac",
                molecule.iupac,
                "https://en.wikipedia.org/wiki/Union_internationale_de_chimie_pure_et_appliqu%C3%A9e",
                "International Union of Pure and Applied Chemistry"
            );
            container.appendChild(ipuacRow);
        }
        if (molecule.inchi) {
            let inchi = molecule.inchi;
            if (inchi instanceof Array) {
                inchi = inchi[0];
            }
            inchi = inchi.replace("InChI=", "");
            container.appendChild(
                this._createDataRow(
                    "InChi",
                    inchi,
                    "https://en.wikipedia.org/wiki/International_Chemical_Identifier",
                    "International Chemical Identifier"
                )
            )
        }
        if (molecule.can) {
            container.appendChild(
                this._createDataRow(
                    "Canonical SMILES ",
                    molecule.can,
                    "https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_Specification",
                    "Simplified Molecular Input Line Entry Specification"
                )
            );
        }
        if (molecule.monoisotopic_mass) {
            container.appendChild(
                this._createDataRow(
                    "Monoisotopic mass",
                    molecule.monoisotopic_mass
                )
            );
        }
        if (molecule.formula) {
            const charge = molecule.charge;
            const formula = molecule.formula;
            let formulaString = "";
            for (let i = formula.length - 1; i >= 0; i--) {
                if (i === formula.length - 1 && charge !== 0) {
                    if (charge > 1 || charge < -1) {
                        formulaString = formula.charAt(i - 1).sup() + formula.charAt(i).sup() + formulaString;
                        i--;
                    } else {
                        formulaString = formula.charAt(i).sup() + formulaString;
                    }
                } else if ($.isNumeric(formula.charAt(i))) {
                    formulaString = formula.charAt(i).sub() + formulaString;
                } else {
                    formulaString = formula.charAt(i) + formulaString;
                }
            }
            container.appendChild(
                this._createDataRow(
                    "Formula",
                    formulaString
                )
            )
        }
        if (molecule.charge !== undefined && molecule.charge !== null) {
            container.appendChild(
                this._createDataRow(
                    "Charge",
                    molecule.charge
                )
            );
        }
        if (molecule.multiplicity !== undefined && molecule.multiplicity !== null){
            container.appendChild(
                this._createDataRow(
                    "Spin multiplicity",
                    molecule.multiplicity
                )
            )
        }

    }

    _createDataRow(label, value, helpLink = null, helpTooltipTitle = null) {
        const element = this._createRowElement();
        const labelColumn = this._createColumnElement();
        labelColumn.classList.add("font-weight-bold");
        labelColumn.appendChild(document.createTextNode(label));
        if (helpLink) {
            const helpLinkElt = document.createElement("a");
            a.href = helpLink;
            a.target = "_blank";
            const innerHelpLink = document.createElement("span");
            if (helpTooltipTitle) {
                innerHelpLink.dataset.placement = "right";
                innerHelpLink.toggle = "tooltip";
                innerHelpLink.title = helpTooltipTitle
            }
            innerHelpLink.innerText = "?"
            helpLinkElt.appendChild(innerHelpLink);
            element.appendChild(helpLinkElt);
        }
        const valueColumn = this._createColumnElement();
        valueColumn.innerText = value;
        element.appendChild(valueColumn);
        return element;
    }

    // noinspection JSMethodCanBeStatic
    _createRowElement(tag = "div") {
        const elt = document.createElement(tag);
        elt.classList.add("row");
        return elt;
    }

    // noinspection JSMethodCanBeStatic
    _createColumnElement(tag = "div") {
        const elt = document.createElement(tag);
        elt.classList.add("col");
        return elt;
    }

}