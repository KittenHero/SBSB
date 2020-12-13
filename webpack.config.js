const path = require('path');
const glob = require('glob');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const PurgecssPlugin = require('purgecss-webpack-plugin');

module.exports = {

  entry: {
    react: './src/react-index.jsx',
    bootstrap: './src/bootstrap-index.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    publicPath: './',
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new HtmlWebpackPlugin({ template: '!!pug-loader!./src/index.pug', filename: 'index.html' }),
    new MiniCssExtractPlugin({ filename: "[name].[contenthash].css" }),
    new PurgecssPlugin({
      paths: [
        path.join(__dirname, 'node_modules/bootstrap/js/dist/collapse.js'),
        path.join(__dirname, 'node_modules/bootstrap/js/dist/modal.js'),
        path.join(__dirname, 'node_modules/bootstrap/js/dist/scrollspy.js'),
        glob.sync(path.join(__dirname, 'src/js/*.js'), { nodir: true }),
        glob.sync(path.join(__dirname, 'src/js/*.jsx'), { nodir: true }),
        glob.sync(path.join(__dirname, 'src/template/*.pug'), { nodir: true }),
      ].flat()
    }),
  ],
  module: {
    rules: [
      {
        test: /\.pug$/,
        exclude: path.resolve(__dirname, 'src/template'),
        use: ['apply-loader', 'pug-loader'],
      },
      {
        test: /\.pug$/,
        include: path.resolve(__dirname, 'src/template'),
        loader: 'pug-loader',
      },
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          }
        },
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader']
      },
      {
        test: /\.(svg|png|ico|jpe?g)$/,
        loader: 'img-optimize-loader',
        options: {
          compress: {
            mode: 'high',
            webp: true,
          }
        }
      },
    ]
  },
  target: 'web',
  devServer: {
    port: 3030,
    contentBase: path.join(__dirname, 'dist'),
    historyApiFallback: true,
  }
}
