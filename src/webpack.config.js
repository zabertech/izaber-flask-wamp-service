var webpack = require('webpack');
var path = require('path');

module.exports = {
  entry: './static/app.js',
  output: {
    path: __dirname + '/static/bundle',
    filename: 'bundle.js'
  },

  resolve: {
    alias: {
      'handsontable': path.join(__dirname, 'node_modules/handsontable/dist/handsontable.full.js'),
      'handsontable.css': path.join(__dirname, 'node_modules/handsontable/dist/handsontable.full.css'),
      'jstree.css': path.join(__dirname, 'node_modules/jstree/dist/themes/default/style.min.css'),
      'jstree-dark.css': path.join(__dirname, 'node_modules/jstree/dist/themes/default-dark/style.min.css'),
      'handlebars' : 'handlebars/dist/handlebars.js'
    }
  },
  module: {
    // noParse: [/handsontable.full.js/],
    rules: [
        { test: /\.css$/, loaders: [ 'style-loader', 'css-loader' ] },
        { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader" },
        { test: /\.(ttf|eot|svg|jpg|gif|png)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader", options: {
            name: '[hash].[ext]',
            outputPath: '',
            publicPath: 'static/',
        } },
    ],
  }
}
