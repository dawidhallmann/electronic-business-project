describe('Register user', () => {
  before(() => {
    cy.visit("")
  });

  it('Go to registratio page', () => {
    cy.clickCheck('.user-info')
    cy.clickCheck('.no-account > a')
  })

  it('Fill registration form', () => {

  })
})