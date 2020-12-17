const path = require('path');
const glob = require('glob');
const webpack = require('webpack');
const dotenv = require('dotenv');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const PurgecssPlugin = require('purgecss-webpack-plugin');

const PROD = process.env.NODE_ENV == 'production';
const config = dotenv.config({ path: path.join(__dirname, PROD ? 'prod.env' : 'dev.env') }).parsed;

module.exports = {
  entry: {
    react: './src/react-index.jsx',
    bootstrap: './src/bootstrap-index.js',
    securepay: './src/securepay.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    publicPath: PROD ? '/' :'./',
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  externals: {
    securepay: 'securePayUI'
  },
  plugins: [
    new webpack.DefinePlugin({
      GOOGLE_API_KEY: JSON.stringify(config.GOOGLE_API_KEY),
      GOOGLE_TAG_KEY: JSON.stringify(config.GOOGLE_TAG_KEY),
      SECUREPAY_CLIENT: JSON.stringify(config.SECUREPAY_CLIENT),
      SECUREPAY_MERCHANT: JSON.stringify(config.SECUREPAY_MERCHANT),
      SECUREPAY_UI: JSON.stringify(PROD
        ? 'https://payments.auspost.net.au/v3/ui/client/securepay-ui.min.js'
        : 'https://payments-stest.npe.auspost.zone/v3/ui/client/securepay-ui.min.js'
      ),
    }),
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
