/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: 'https://cleanroomlabs.dev',
  generateRobotsTxt: false,  // We have a manual robots.txt
  exclude: ['/docs/*'],      // Sphinx generates its own sitemap
  additionalPaths: async (config) => [
    // Add any additional paths here
  ],
};
