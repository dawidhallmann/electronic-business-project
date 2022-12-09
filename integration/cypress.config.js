const { defineConfig } = require("cypress");

module.exports = defineConfig({
  viewportHeight: 1080,
  viewportWidth: 1920,
  defaultCommandTimeout: 8000,
  requestTimeout: 20000,
  watchForFileChanges: false,
  e2e: {
    baseUrl: 'http://localhost:8080/',
    specPattern: "cypress/specs/**/*.cy.{js,jsx,ts,tsx}",
    experimentalRunAllSpecs: true,
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
