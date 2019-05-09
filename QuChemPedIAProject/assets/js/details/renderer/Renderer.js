export default class {

    /**
     * @abstract
     * @param {*} data
     * @param {HTMLElement} rootElement
     */
    render(data, rootElement) {
        throw new Error("Must be implemented in subclass");
    }
}