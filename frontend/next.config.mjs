/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ["plotly.js", "react-plotly.js"],
  webpack: (config, { isServer }) => {
    // Web Workers: Next.js 14 handles *.worker.ts natively via
    // `new Worker(new URL('./stats.worker.ts', import.meta.url))`
    // — no worker-loader plugin needed.

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
