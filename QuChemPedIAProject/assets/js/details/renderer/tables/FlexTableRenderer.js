import TableRenderer from "./TableRenderer";

export default class FlexTableRenderer extends TableRenderer{


    createDataColBaseHtmlElement() {
        const col = document.createElement("div");
        col.classList.add("col");

        return col;
    }

    createDataRowBaseHtmlElement() {
            const row = document.createElement("div")
            row.classList.add("row");
        return row;
    }

    createHeaderColBaseHtmlElement() {
        const headerColumn = document.createElement("div")
        headerColumn.classList.add("col");
        return headerColumn;
    }

    createHeaderRowBaseHtlmElement() {
        const headerRow = document.createElement("div");
        headerRow.classList.add("row");

        return headerRow;
    }
}