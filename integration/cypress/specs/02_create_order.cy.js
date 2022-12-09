describe('Create order', () => {
  before(() => {
    cy.visit("")
    cy.login()
  });

  it('Order products', () => {
    // add products to backet
    cy.addProduct('a[href*=533-]', "3")
    cy.visit("")
    cy.addProduct('a[href*=538-]')
    cy.clickCheck('.blockcart')

    // remove second product from basket
    cy.clickCheck(':nth-child(2) a.remove-from-cart')
    cy.clickCheck('.cart-summary a.btn')

    cy.ifExists('.delete-address', () => {
      cy.clickCheck(".delete-address")
      cy.wait(2000)
      cy.visit("zam%C3%B3wienie")
    })

    // fill address form
    cy.typeCheck('#field-address1', "Olimpijska 2")
    cy.typeCheck('#field-postcode', "83-359")
    cy.typeCheck('#field-city', "Gdynia")
    cy.clickCheck('.form-footer > .continue')
    cy.wait(2000)
    cy.visit("zam%C3%B3wienie")

    cy.clickCheck('#js-delivery > .continue')
    cy.wait(2000)
    cy.visit("zam%C3%B3wienie")

    cy.clickCheck('#payment-option-1-container')
    cy.get('.custom-checkbox input').click({force: true})
    cy.clickCheck('.ps-shown-by-js > .btn')
  })
})