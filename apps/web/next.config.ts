import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@clinic/database"],
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "lh3.googleusercontent.com" },
    ],
  },
};

export default nextConfig;
