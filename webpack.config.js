const path = require('path');
const glob = require('glob');
const webpack = require('webpack');
const dotenv = require('dotenv');
const sveltePreprocess = require('svelte-preprocess');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const PROD = process.env.NODE_ENV == 'production';
const config = dotenv.config({ path: path.join(__dirname, PROD ? 'prod.env' : 'dev.env') }).parsed;
const jsconfig = {
  GOOGLE_API_KEY: JSON.stringify(config.GOOGLE_API_KEY),
  GOOGLE_TAG_KEY: JSON.stringify(config.GOOGLE_TAG_KEY),
  SECUREPAY_CLIENT: JSON.stringify(config.SECUREPAY_CLIENT),
  SECUREPAY_MERCHANT: JSON.stringify(config.SECUREPAY_MERCHANT),
  API_URL: JSON.stringify(config.API_URL),
  SECUREPAY_UI: JSON.stringify(PROD
    ? 'https://payments.auspost.net.au/v3/ui/client/securepay-ui.min.js'
    : 'https://payments-stest.npe.auspost.zone/v3/ui/client/securepay-ui.min.js'
  ),
};

module.exports = {
  target: 'web',
  // devtool: 'source-map',
  entry: {
    main: './src/main.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    publicPath: PROD ? '/' :'./',
  },
  resolve: {
    extensions: ['.js', '.svelte'],
    mainFields: ['svelte', 'browser', 'module', 'main']
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/prerender.js',
      scriptLoading: 'defer',
    }),
    new MiniCssExtractPlugin({ filename: "[name].[contenthash].css" }),
  ],
  module: {
    rules: [
      {
        test: /\.svelte$/,
        resolve: {
          fullySpecified: false,
        },
        use: function(info) {
          const loader = {
            loader: 'svelte-loader',
            options: {
              hotReload: !PROD,
              hydratable: true,
              // emitCss: true,
              preprocess: info.resource.startsWith(path.resolve(__dirname, 'src'))
                ? sveltePreprocess({
                  defaults: {
                    markup: 'pug',
                    script: 'javascript',
                    style: 'less',
                  },
                  replace: Object.entries(jsconfig).map(([k, v]) => [new RegExp(k, 'g'), v]),
                })
                : {},
            }
          };
          if (info.compiler === 'HtmlWebpackCompiler') {
            Object.assign(loader.options, {
              generate:  'ssr',
              hotReload: false,
              css: true,
            });
          }
          return loader;
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
      {
        test: /\.(woff2?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        exclude: path.resolve(__dirname, 'src/assets/img'),
        use: {
          loader: 'file-loader',
          options: {
            outputPath: 'fonts/'
          }
        }
      },
    ]
  },
  devServer: {
    port: 3000,
    contentBase: path.join(__dirname, 'dist'),
    historyApiFallback: true,
  }
}
