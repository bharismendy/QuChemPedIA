const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const CopyWebpackPlugin = require('copy-webpack-plugin')

const copyPlugin =     new CopyWebpackPlugin([
    { from: './assets/resources/**', to: './resources', flatten: true}
], {})

module.exports = {
    context: __dirname,
    entry: {
        main: ['./assets/js/main.js', './assets/scss/main.scss'],
    },
    output: {
        path: path.resolve('./static'),
        filename: "[name]-[hash].js"
    },
    module: {
        rules: [{
            test: /\.scss$/,
            use: [
                "style-loader", // creates style nodes from JS strings
                "css-loader", // translates CSS into CommonJS
                "sass-loader" // compiles Sass to CSS, using Node Sass by default
            ]
        }]
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        copyPlugin
    ]
}
