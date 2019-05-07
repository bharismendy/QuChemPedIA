import SmilesDrawer from "smiles-drawer"

export default class MoleculeSmilesRenderer {

    constructor() {
    }

    render(molecule, rootElement) {
        if (!molecule.can) {
            return;
        }
        const canvas = document.createElement("canvas");
        canvas.innerText = "Sorry, your browser doesn't support the &lt;canvas&gt; element."
        canvas.height = 300;
        canvas.width = 300;
        canvas.id = "molecule-canvas";
        rootElement.appendChild(canvas);

        let options = {};

        // Initialize the drawer
        let smilesDrawer = new SmilesDrawer.Drawer(options);

        SmilesDrawer.parse(molecule.can, function (tree) {
            // Draw to the canvas
            smilesDrawer.draw(tree, 'canvas', 'light', false);
        });
    }

}