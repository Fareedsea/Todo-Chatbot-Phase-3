import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  experimental: {
    optimizePackageImports: [
      '@tanstack/react-query',
      'better-auth',
    ],
  },
};

export default nextConfig;
