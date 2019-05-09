/**
 * @external AuthorRepository
 */

/**
 * @external CardRenderer
 */

/**
 * @external TableRenderer
 */

/**
 *
 */
export default class AssociatedCalculationRenderer{
    /**
     *
     * @param {AuthorRepository} authorRepository
     * @param {CardRenderer} cardRenderer
     * @param {TableRenderer} tableRenderer
     */
    constructor(authorRepository, cardRenderer, tableRenderer) {
        this._authorRepository = authorRepository;
        this._cardRenderer = cardRenderer
        this._tableRenderer = tableRenderer
    }

    render (data, rootElement) {
        this._cardRenderer.render({
            headerRenderCallback: this._renderHeader,
            bodyRenderCallback: this._renderBody,
            data
        },
        rootElement);
    }

    // noinspection JSMethodCanBeStatic
    _renderHeader(data, cardHeader) {
        cardHeader.innerHTML = "<h5>Associated Calculations</h5>";
    }

    _renderBody(data, rootElement) {
        const labels = [
            {
                headerInnerHtml: "Job Type",
                key: "job_type",
                headerClasses: ['my-auto', "font-weight-bold"],
                columnClasses: ['my-auto']
            },
            {
                headerInnerHtml: "Author",
                key: "author",
                headerClasses: ['my-auto', "font-weight-bold"],
                columnClasses: ['my-auto'],
                columnRenderCallback: (object, rootElement) => {
                    this._authorRepository.findAuthorById(object.author_id)
                        .then((author) => {
                            return author.name
                        })
                        .catch((err) => {
                            return "N/A"
                        })
                        .then((name) => {
                            rootElement.innerHTML = `<span>${name}</span>`
                        });
                }
            },
            {
                headerInnerHtml: "Description",
                key: "description",
                headerClasses: ['my-auto', "font-weight-bold"],
                columnClasses: ['my-auto'],
                columnRenderCallback: (object, rootElement) => {
                    // TODO add click event on button
                    rootElement.innerHTML = `<button type="button" style="background-color:transparent" id="key" class="btn btn-primary-outline myButton">
                            <span class="fa fa-file-text" aria-hidden="true"></span>
                        </button>`
                }
            },
        ];

        // siblings might have other siblings we have to print - So we flatten the array
        const flattenedSiblings = this._flattenSibling(data.siblings);

        const tableData = flattenedSiblings.map((sibling) => {
            return {
                job_type: sibling.job_type,
                author_id: sibling.data.metadata.id_user
            }
        });


        this._tableRenderer.render({labelsDescriptions: labels, data: tableData, opt: {}}, rootElement);

    }

    _flattenSibling(siblings) {
        return siblings.reduce((acc, sibling) => {
                acc.push(sibling);
                if (sibling.job_type === "TD") {
                    const siblingSiblings = sibling.siblings.map((s) => {
                        const obj = Object.assign({}, s);
                        obj.job_type = "";
                        return obj;
                    });
                    Array.prototype.push.apply(acc, siblingSiblings)
                }
                return acc;
            },
            []
        );
    }
}