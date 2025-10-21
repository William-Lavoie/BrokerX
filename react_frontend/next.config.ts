/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/auth/:path*',
        destination: 'http://keycloak:7080/auth/:path*',
      },
      {
        source: '/realms/:path*',
        destination: 'http://keycloak:7080/realms/:path*',
      },
    ];
  },
};

export default nextConfig;
