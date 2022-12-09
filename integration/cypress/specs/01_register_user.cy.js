describe('Register user', () => {
  before(() => {
    cy.visit("")
  });

  it('Register user', () => {
    cy.clickCheck('.user-info')
    cy.clickCheck('.no-account > a')

    cy.clickCheck('[for="field-id_gender-1"] > .custom-radio')
    cy.typeCheck('#field-firstname', "Jan")
    cy.typeCheck('#field-lastname', "Kowalski")
    cy.typeCheck('#field-email', "jan_kowalski@gmail.com")
    cy.typeCheck('#field-password', "Str0nkP@ss")
    cy.get(':nth-child(8) > .col-md-6 > .custom-checkbox > label > input')
      .should("exist")
      .click({force: true})
    cy.clickCheck('.form-footer > .btn')
  })
})