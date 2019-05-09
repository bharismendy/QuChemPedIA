export default class MoleculeSidebarRenderer {
    constructor() {

    }

    /**
     * @param {*} moleculeData
     * @param {HTMLElement} rootElement
     */
    render(moleculeData, rootElement) {
        rootElement.classList.add("card", "sidenav");
        const closeButton = document.createElement('div');
        closeButton.id = "closebtn"
        closeButton.textContent = "&times;"

        closeButton.addEventListener('click', () => {
            rootElement.classList.add("d-none");
        });

        rootElement.appendChild(closeButton);

        if (moleculeData.molecule) {
            rootElement.appendChild(
                this._createMenuElement("#Molecule", "Molecule")
            );
        }
        if (moleculeData.metadata) {
            rootElement.appendChild(
                this._createMenuElement("#associatedCalculations", "Associated calculations")
            );
            rootElement.appendChild(
                this._createMenuElement("#Authorship", "Authorship")
            );
        }

        if (moleculeData.comp_details) {
            rootElement.appendChild(
                this._createMenuElement("#ComputationalDetails", "Computational Details")
            );
        }

        if (moleculeData.results) {
            rootElement.appendChild(
                this._createMenuElement("#Results", "Results")
            );

            if (moleculeData.results.geometry) {
                rootElement.appendChild(
                    this._createMenuElement("#Geometry", "Geometry")
                );
            }

            if (moleculeData.results.freq) {
                rootElement.appendChild(
                    this._createMenuElement("#Thermochemistry", "Thermochemistry")
                );
            }

            if (moleculeData.results.excited_states) {
                rootElement.appendChild(
                    this._createMenuElement("ExcitedStates", "Excited States")
                );
            }
        }

        // TODO event handling
    }

    _createMenuElement(href, label) {
        const link = document.createElement("a");
        link.href = "href";

        const row = document.createElement("div");
        row.classList.add("row");
        row.id = "_associatedCalculations";

        row.appendChild(this._createFlaskLinkElement());
        link.appendChild(row);

        const titleCol = document.createElement("div")
        titleCol.classList.add("col-lg-10");
        titleCol.innerText = label;

        link.appendChild(titleCol);

        return link;
    }

    // noinspection JSMethodCanBeStatic
    _createFlaskLinkElement() {
        const element = document.createElement("div");
        const child1 = document.createElement("div");
        const child2 = document.createElement("div");

        element.classList.add("col-lg-1");

        child1.classList.add("fa fa-flask flaskChem1");
        child2.classList.add("fa fa-flask flaskChem");

        element.appendChild(child1);
        element.appendChild(child2);
        return element;
    }
}