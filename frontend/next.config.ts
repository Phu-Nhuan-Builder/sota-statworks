import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["plotly.js", "react-plotly.js"],
  webpack: (config, { isServer }) => {
    // Web Worker support
    config.module.rules.push({
      test: /\.worker\.(ts|js)$/,
      use: {
        loader: "worker-loader",
        options: {
          filename: "static/[hash].worker.js",
        },
      },
    });

    // Fallback for node modules not available in browser
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }

    return config;
  },
};

export default nextConfig;
