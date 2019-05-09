import Renderer from "../Renderer";

export default class MoleculeGeometryRenderer extends Renderer {

    /**
     *
     * @param {Renderer} [convergenceTableRenderer]
     */
    constructor(convergenceTableRenderer) {
        super();
        this.convergenceTableRenderer = convergenceTableRenderer;
    }

    render(data, rootElement) {
        const subCardHtmlElement = document.createElement("div");
        subCardHtmlElement.classList.add("container", "subCard");
        subCardHtmlElement.id = "Geometry";

        const titleElement = document.createElement("h5");
        titleElement.classList.add("card-title", "subTitle");
        titleElement.innerText = "Geometry";

        subCardHtmlElement.appendChild(titleElement);

        const container = document.createElement("div");

        if (data.results.geometry.nuclear_repulsion_energy_from_xyz) {
            container.appendChild(
                this._createNuclearRepulsionEnergyViz(
                    results.results.geometry.nuclear_repulsion_energy_from_xyz
                )
            );
        }

        if (this.convergenceTableRenderer) {
            this.convergenceTableRenderer.render(data, subCardHtmlElement);
        }
    }

    // noinspection JSMethodCanBeStatic
    _createNuclearRepulsionEnergyViz(nuclear_repulsion_energy_from_xyz) {
        const row = document.createElement("div");
        row.classList.add("row");
        const colLabel = document.createElement("div");
        colLabel.classList.add("col", "font-weight-bold");
        colLabel.innerText = "Nuclear repulsion energy in atomic units"

        const colValue = document.createElement("div");
        colValue.classList.add("col");
        colValue.innerText = nuclear_repulsion_energy_from_xyz;

        row.appendChild(colLabel);
        row.appendChild(colValue);
        return row;
    }
}