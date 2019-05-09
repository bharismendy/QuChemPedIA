export default class CardRenderer {

    /**
     * @callback RenderCallback
     * @param {Object} data
     * @param {HTMLElement} rootElement
     */

    /**
     *
     * @param {RenderCallback} headerRenderCallBack
     * @param {RenderCallback} bodyRenderCallback
     */
    constructor(headerRenderCallBack, bodyRenderCallback) {
        this._headerRenderCallback = headerRenderCallBack;
        this._bodyRenderCallback = bodyRenderCallback;
    }

    render (data, rootElement) {
        const cardElement = document.createElement("div");
        cardElement.classList.add("card");

        const header = document.createElement("div");
        header.classList.add("card-header");
        this._headerRenderCallback(data, header);

        cardElement.appendChild(header);

        const body = document.createElement("div");
        body.classList.add("container");
        this._bodyRenderCallback(data, body);
        cardElement.appendChild(body);

        rootElement.appendChild(cardElement);
    }

}