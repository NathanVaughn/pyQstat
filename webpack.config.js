const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = {
    entry: './pyQstat/src/js/index.js',
    output: {
        filename: 'js/bundle.js',
        path: path.resolve(__dirname, './pyQstat/dist/')
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/main.css',
        }),
        new OptimizeCssAssetsPlugin({
            assetNameRegExp: /\.css$/,
            cssProcessor: require('cssnano'),
            cssProcessorPluginOptions: {
              preset: ['default', { discardComments: { removeAll: true } }],
            },
            canPrint: true
          })
    ],
    module: {
        rules: [{
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader"
                ]
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            }
        ]
    },
};