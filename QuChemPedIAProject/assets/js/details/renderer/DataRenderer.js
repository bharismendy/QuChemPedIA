import {valueFromPath} from "../../utils";

export default class DataRenderer {

    /**
     * @callback RenderFunction
     * @param {*} data
     * @param {HTMLElement} rootElement
     * @param {Object} [options]
     */

    /**
     * @typedef Renderer
     * @property {RenderFunction} render
     */

    /**
     * @typedef RenderConfig
     * @property {String} dataKey
     * @property {Renderer} renderer
     * @property {String} htmlTag
     * @property {Object} renderOptions
     * @property {String[]} classes
     */

    /**
     * @param {RenderConfig[]} renderers
     */
    constructor(renderers) {
       this._renderers = renderers;
    }

    /**
     *
     * @param {Object} data
     * @param {HTMLElement} rootElement
     */
    render(data, rootElement){
        this._renderers.forEach((config) => {

            if (!config.dataKey || !config.renderer){
                return;
            }

            const htmlTag = config.htmlTag  || 'div';

            const subData = valueFromPath(data, config.dataKey);

            if(subData === undefined) {
                // throw new Error('Invalid object: path ' + config.dataKey + ' does not exists in the data object')
                return;
            }

            const childElement = document.createElement(htmlTag);
            if (config.classes) {
                childElement.classList.add.apply(childElement.classList, config.classes)
            }
            config.renderer.render(subData, childElement, config.renderOptions);
            rootElement.appendChild(childElement);
        })
    }
}