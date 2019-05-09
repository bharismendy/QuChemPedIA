import TableRenderer from "./TableRenderer";

export default class HtmlTableRenderer extends TableRenderer {

    createDataColBaseHtmlElement() {
        return document.createElement("td");
    }

    createDataRowBaseHtmlElement() {
        return document.createElement("tr");
    }

    createHeaderColBaseHtmlElement() {
        return document.createElement("th");
    }

    createHeaderRowBaseHtlmElement() {
        return document.createElement("tr");
    }

    createBaseHtmlElement() {
        return document.createElement("table");
    }
}