var config = require('./webpack.config.js');
var BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

const copyPlugin = new CopyWebpackPlugin([
  { from: './assets/resources/**', to: './resources', flatten: false }
], {})


config.output.path = require('path').resolve('./common_qcpia/static/dist');
config.output.filename = "[name]-[hash].js";

config.plugins = [
      new VueLoaderPlugin(),
  copyPlugin,
    new BundleTracker({filename: './webpack-stats-prod.json'})
];



module.exports = config;