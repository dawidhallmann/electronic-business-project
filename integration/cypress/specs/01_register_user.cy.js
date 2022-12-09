import {USER_EMAIL, USER_PASSWORD} from "../support/e2e"

describe('Auth', () => {
  beforeEach(() => {
    cy.visit("")
  });

  it('Register user', () => {
    cy.clickCheck('.user-info')
    cy.clickCheck('.no-account > a')

    cy.clickCheck('[for="field-id_gender-1"] > .custom-radio')
    cy.typeCheck('#field-firstname', "Jan")
    cy.typeCheck('#field-lastname', "Kowalski")
    cy.typeCheck('#field-email', USER_EMAIL)
    cy.typeCheck('#field-password', USER_PASSWORD)
    cy.get(':nth-child(8) > .col-md-6 > .custom-checkbox > label > input')
      .should("exist")
      .click({force: true})
    cy.clickCheck('.form-footer > .btn')
  })

  it('Log in / log out', () => {
    cy.login()
    cy.clickCheck('.logout')
  })
})