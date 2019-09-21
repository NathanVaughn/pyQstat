const path = require('path');
const glob = require('glob');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const PATHS = {
    // setup some basic useful paths
    src: path.join(__dirname, 'app', 'src'),
    dist: path.join(__dirname, 'app', 'dist')
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