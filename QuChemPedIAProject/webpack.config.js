const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const VueLoaderPlugin = require('vue-loader/lib/plugin')

const copyPlugin = new CopyWebpackPlugin([
  { from: './assets/resources/**', to: './resources', flatten: false }
], {})

module.exports = {
  context: __dirname,
  entry: {
    main: ['./assets/js/main.js', './assets/scss/main.scss'],
    details: ['./assets/js/details/main.js'],
    viz: ['./assets/js/viz/main.js']
  },
  output: {
    path: path.resolve('./common_qcpia/static/webpack_bundles/'),
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.(js|vue)$/,
        exclude: /node_modules/,
        loader: 'eslint-loader'
      },
      {
        test: /\.scss$/,
        use: [
          'style-loader', // creates style nodes from JS strings
          'css-loader', // translates CSS into CommonJS
          'sass-loader' // compiles Sass to CSS, using Node Sass by default
        ]
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
    }
  },
  plugins: [
    new VueLoaderPlugin(),
    new BundleTracker({ filename: './webpack-stats.json' }),
    copyPlugin
  ]
}
