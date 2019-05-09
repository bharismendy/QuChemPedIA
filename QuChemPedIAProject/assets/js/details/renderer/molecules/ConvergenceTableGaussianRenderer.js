import Renderer from "../Renderer";

export class ConvergenceTableGaussianRenderer extends Renderer {

    constructor(tableRenderer) {
        super();
        this._tableRenderer = tableRenderer;
    }

    render(data, rootElement) {
        if(!(results.comp_details.general.package
            && (results.comp_details.general.package === "Gaussian"))){
            throw new Error("Can't use ConvergenceTableGaussianRenderer with this set of data");
        }


        if(data.comp_details.geometry.geometric_targets) {

            const introText = document.createElement("p");
            introText.innerText = "This calculation is the result of a geometry optimization process.";

            const geometric_targets = results.comp_details.geometry.geometric_targets;
            const geometric_values = results.results.geometry.geometric_values[results.results.geometry.geometric_values.length - 1];
            const titreCols = [
                "Maximum Force"
                , "RMS Force"
                , "Maximum Displacement"
                , "RMS Displacement"
            ];

            const subCard = document.createElement("div");
            subCard.classList.add("container", "subWavefunction");
            subCard.align = "center";

            const subCardTitle = document.createElement("span");
            subCardTitle.classList.add("font-weight-bold");
            subCardTitle.innerText = "Geometry optimization convergence criteria";
            subCard.appendChild(subCardTitle);

            const labelsDescriptions = [
                { headerInnerHtml: "", key: "label", columnClasses: ["cellulTitre"]},
                { headerInnerHtml: "Value", key: "value"},
                { headerInnerHtml: "Threshold", key: "target"}
            ];

            const tableData = titreCols.map((label, index) => {
                return {
                    label,
                    value: geometric_values[index],
                    target: geometric_targets[index]
                }
            });

            this._tableRenderer.render({
                labelsDescriptions,
                data: tableData,
                opt: {}
            }, subCard);


        }
    }
}