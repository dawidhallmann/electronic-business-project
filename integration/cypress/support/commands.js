// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

export const USER_EMAIL="jan-kowalski@gmail.com"
export const USER_PASSWORD="Str0nkP@ss"

Cypress.Commands.overwrite("visit", (originalFn, url, options) => {
    const { baseUrl } = Cypress.config();
    return originalFn(`${baseUrl}${url || ""}`, {
      ...(options || {}),
    });
});

Cypress.Commands.add("clickCheck", (selector) => {
    cy.get(selector)
      .should("exist")
      .first()
      .scrollIntoView()
      .click()
});

Cypress.Commands.add("typeCheck", (selector, value) => {
    cy.get(selector)
      .should("be.visible")
      .type(value)
});

Cypress.Commands.add("addProduct", (selector, amount="1") => {
    cy.clickCheck(selector)
    cy.typeCheck('#quantity_wanted', "{selectAll}" + amount)
    cy.clickCheck('.add > .btn')
    cy.clickCheck('.cart-content-btn > .btn-secondary')
});

Cypress.Commands.add("login", () => {
    cy.clickCheck('.user-info')
    cy.typeCheck('#field-email', USER_EMAIL)
    cy.typeCheck('#field-password', USER_PASSWORD)
    cy.clickCheck('#submit-login')
});

Cypress.Commands.add("ifExists", (selector, successCallback) => {
    cy.wait(500);
    cy.document().then((doc) => {
      const documentResult = doc.querySelectorAll(selector);
      if (documentResult.length) {
        successCallback();
      }
    });
});  
  
Cypress.on("uncaught:exception", (err, runnable) => {
    return false;
});
