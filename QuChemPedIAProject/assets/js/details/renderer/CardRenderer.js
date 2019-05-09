// Bootstrap4 card classes - See https://getbootstrap.com/docs/4.3/components/card/
export const CARD_CLASSES = ["card"];
export const CARD_HEADER_CLASSES = ["card-header"];
export const CARD_BODY_CLASSES = ["card-body"];
export const CARD_FOOTER_CLASSES = ["card-footer"];

export default class CardRenderer {

    /**
     *
     * @param {String[]} [classes]
     * @param {String[]} [headerClasses]
     * @param {String[]} [bodyClasses]
     * @param {String[]} [footerClasses]
     */
    constructor({classes = [], headerClasses = [], bodyClasses = [], footerClasses = []}) {
        this._classes = classes.concat(CARD_CLASSES);
        this._headerClasses = headerClasses.concat(CARD_HEADER_CLASSES);
        this._bodyClasses = bodyClasses.concat(CARD_BODY_CLASSES);
        this._footerClasses = footerClasses.concat(CARD_FOOTER_CLASSES);
    }

    /**
     * @callback RenderCallback
     * @param {Object} data
     * @param {HTMLElement} rootElement
     */

    /**
     * @param {RenderCallback} [headerRenderCallBack] Function rendering the card header
     * @param {RenderCallback} [bodyRenderCallback] Function rendering the card body
     * @param {RenderCallback} [footerRenderCallback] Function rendering the card footer
     * @param {*} data Data argument passed to the RenderCallback functions
     * @param {HTMLElement} rootElement
     */
    render({headerRenderCallback, bodyRenderCallback, footerRenderCallback, data}, rootElement) {
        const cardElement = document.createElement("div");
        DOMTokenList.prototype.add.apply(cardElement.classList, this._classes);

        if (headerRenderCallback) {
            const header = document.createElement("div");
            DOMTokenList.prototype.add.apply(header.classList, this._headerClasses);
            headerRenderCallback(data, header);
        }

        cardElement.appendChild(header);

        if (bodyRenderCallback) {
            const body = document.createElement("div");
            DOMTokenList.prototype.add.apply(body.classList, this._bodyClasses);
            bodyRenderCallback(data, body);
            cardElement.appendChild(body);

            rootElement.appendChild(cardElement);
        }

        if (footerRenderCallback) {
            const footer = document.createElement("div");
            DOMTokenList.prototype.add.apply(footer.classList, this._footerClasses);
            footerRenderCallback(data, footer);
        }

        rootElement.appendChild(cardElement);
    }
}