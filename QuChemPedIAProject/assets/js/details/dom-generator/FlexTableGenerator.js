/**
 * @callback ColumnRenderCallback
 * @param {Object} data
 * @param {HTMLElement} rootElement
 */

/**
 * @typedef LabelDescription
 * @property {String|HTMLElement} headerInnerHtml
 * @property {String} key
 * @property {String[]} [columnClasses]
 * @property {String[]} [headerClasses]
 * @property {ColumnRenderCallback} columnRenderCallback
 */

/**
 * @typedef GenerationOption
 * @property columnClasses
 */

/**
 *
 * @param {LabelDescription[]} labelsDescriptions
 * @param {Object[]} data
 * @param {GenerationOption} opt
 * @returns {HTMLDivElement}
 */
export const generateTable = (labelsDescriptions, data, opt) => {
    const root = document.createElement("div");
    root.classList.add("container");

    const headerRow = document.createElement("div");
    headerRow.classList.add("row");

    labelsDescriptions.forEach((labelDescription) => {
        const headerColumn = document.createElement("div")
        headerColumn.classList.add("col");

        if (labelDescription.headerInnerHtml instanceof String){
            headerColumn.innerHTML = labelDescription.headerInnerHtml;
        }else {
            headerColumn.appendChild(labelDescription.headerInnerHtml);
        }

        headerRow.appendChild(headerColumn);
    });

    data.forEach( object => {
        const row = document.createElement("div")
        row.classList.add("row");

        labelsDescriptions.forEach((labelDescription) => {
            const col = document.createElement("div");
            col.classList.add("col");
            if (labelDescription.columnClasses){
                DOMTokenList.prototype.add.apply(col.classList, labelDescription.columnClasses)
            }
            if (opt.columnClasses) {
                DOMTokenList.prototype.add.apply(col.classList, opt.columnClasses);
            }
            if (labelDescription.columnRenderCallback !== undefined){
                labelDescription.columnRenderCallback(object, col);
            } else if (object.hasOwnProperty(labelDescription.key)){
                col.innerText = object[labelDescription.key]
            }
            row.appendChild(col);
        });
    });

    return root;
};