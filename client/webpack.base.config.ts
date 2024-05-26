import path from "path";
import { Configuration } from "webpack";
import MiniCssExtractPlugin from "mini-css-extract-plugin";

const config: Configuration = {
  stats: "minimal",
  entry: {
    wagtailadmin_login: "./src/wagtailadmin_login.ts",
    wagtail_mfa: "./src/wagtail_mfa.ts",
  },
  plugins: [new MiniCssExtractPlugin()],
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.scss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          // Translates CSS into CommonJS
          "css-loader",
          // Compiles Sass to CSS
          "sass-loader",
        ],
      },
    ],
  },
  resolve: {
    extensions: [".ts", ".js"],
  },
  output: {
    path: path.resolve("../src/wagtail_mfa/static/wagtail_mfa"),
  },
};

export default config;
