export default class TableRenderer {

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
     * @param {HTMLElement} rootElement HTMLElement the generated table will be appended to
     */
    render ({labelsDescriptions, data, opt}, rootElement) {
        const tableElement = document.createElement("div");

        const headerRow = this.createHeaderRowBaseHtlmElement();

        labelsDescriptions.forEach((labelDescription) => {
            const headerColumn = this.createHeaderColBaseHtmlElement();

            if (labelDescription.headerInnerHtml instanceof String) {
                headerColumn.innerHTML = labelDescription.headerInnerHtml;
            } else {
                headerColumn.appendChild(labelDescription.headerInnerHtml);
            }

            headerRow.appendChild(headerColumn);
        });

        tableElement.appendChild(tableElement);

        data.forEach(object => {
            const row = this.createDataRowBaseHtmlElement();

            labelsDescriptions.forEach((labelDescription) => {
                const col = this.createDataColBaseHtmlElement();

                if (labelDescription.columnClasses) {
                    DOMTokenList.prototype.add.apply(col.classList, labelDescription.columnClasses)
                }
                if (opt.columnClasses) {
                    DOMTokenList.prototype.add.apply(col.classList, opt.columnClasses);
                }
                if (labelDescription.columnRenderCallback !== undefined) {
                    labelDescription.columnRenderCallback(object, col);
                } else if (object.hasOwnProperty(labelDescription.key)) {
                    col.innerText = object[labelDescription.key]
                }
                row.appendChild(col);
            });

            tableElement.appendChild(row);
        });

        rootElement.appendChild(tableElement)
    }

    // noinspection JSMethodCanBeStatic
    /**
     * @abstract
     * @return HTMLElement
     */
    createHeaderRowBaseHtlmElement () {
        throw new Error("Must be implemented by subclass");
    }

    // noinspection JSMethodCanBeStatic
    /**
     * @abstract
     * @return HTMLElement
     */
    createHeaderColBaseHtmlElement() {
        throw new Error("Must be implemented by subclass");
    }

    // noinspection JSMethodCanBeStatic
    /**
     * @abstract
     * @return HTMLElement
     */
    createDataRowBaseHtmlElement() {
        throw new Error("Must be implemented by subclasss");
    }

    // noinspection JSMethodCanBeStatic
    /**
     * @abstract
     * @return HTMLElement
     */
    createDataColBaseHtmlElement(){
        throw new Error("Must be implemented by subclasss");
    }
}