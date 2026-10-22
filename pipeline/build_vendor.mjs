// Bundles the official Anthropic SDK into one browser file for the Sidekick chat (run: node pipeline/build_vendor.mjs).
// Node-only modules the SDK touches for server credentials are stubbed out; the browser never uses them.
import { build } from "esbuild";

await build({
  stdin: { contents: 'export { default } from "@anthropic-ai/sdk";', resolveDir: process.cwd() },
  bundle: true, format: "esm", platform: "browser", minify: true,
  outfile: "site_src/assets/vendor/anthropic-sdk.mjs",
  plugins: [{
    name: "stub-node",
    setup(b) {
      b.onResolve({ filter: /^node:/ }, (a) => ({ path: a.path, namespace: "stub" }));
      b.onLoad({ filter: /.*/, namespace: "stub" }, () => ({ contents: "module.exports = {};", loader: "js" }));
    },
  }],
});
console.log("wrote site_src/assets/vendor/anthropic-sdk.mjs");
