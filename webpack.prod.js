const path = require('path');
const glob = require('glob');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const PurgecssPlugin = require('purgecss-webpack-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const PATHS = {
    // setup some basic useful paths
    src: path.join(__dirname, 'pyQstat', 'src'),
    dist: path.join(__dirname, 'pyQstat', 'dist')
};

module.exports = {
    // main entry file
    entry: path.join(PATHS.src, 'js/index.js'),
    // output file
    output: {
        filename: 'js/bundle.js',
        path: PATHS.dist
    },
    plugins: [
        // extract css
        new MiniCssExtractPlugin({
            filename: 'css/main.css',
        }),
        // remove extra css
        new PurgecssPlugin({
            paths: glob.sync('pyQstat/**/*', {
                nodir: true
            }),
        }),
        // minify css
        new OptimizeCssAssetsPlugin({
            assetNameRegExp: /\.css$/,
            cssProcessor: require('cssnano'),
            cssProcessorPluginOptions: {
                preset: ['default', {
                    discardComments: {
                        removeAll: true
                    }
                }],
            },
            canPrint: true
        })
    ],
    module: {
        rules: [{
                // css loader
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader"
                ]
            },
            {
                // run js through Babel
                test: /\.js$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            }
        ]
    },
};