var path = require("path");
var webpack = require("webpack");
var APP_DIR = path.resolve(__dirname, "./ui/assets/js/src");
var BUILD_DIR = path.resolve(__dirname, "./dist");

module.exports = {
  entry: APP_DIR + "/App.js",
  output: {
    path: BUILD_DIR,
    filename: "bundle.js"
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        use: "babel-loader"
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
  },
  resolve: {
    extensions: [".js", ".jsx", ".css"]
  },
  plugins: [new webpack.optimize.UglifyJsPlugin({ minimize: true })]
};