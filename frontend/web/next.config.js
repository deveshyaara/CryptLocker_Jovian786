/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  poweredByHeader: false,
  output: 'standalone',
  images: {
    domains: ['localhost'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8031',
    NEXT_PUBLIC_HOLDER_API_URL: process.env.NEXT_PUBLIC_HOLDER_API_URL || 'http://localhost:8031',
    NEXT_PUBLIC_ISSUER_API_URL: process.env.NEXT_PUBLIC_ISSUER_API_URL || 'http://localhost:8030',
    NEXT_PUBLIC_VERIFIER_API_URL: process.env.NEXT_PUBLIC_VERIFIER_API_URL || 'http://localhost:8032',
  },
  async rewrites() {
    return [
      {
        source: '/api/holder/:path*',
        destination: `${process.env.NEXT_PUBLIC_HOLDER_API_URL || 'http://localhost:8031'}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
