describe('Create order', () => {
  beforeEach(() => {
    cy.visit("")
    cy.login()
  });

  it('Order products', () => {
    // add products to backet
    [...Array(5).keys()].forEach(i => {
      cy.clickCheck('#category-3 > .dropdown-item');
      cy.addProduct(`.products .product:nth-child(${i+1})`, (i+1).toString())
    });
    [...Array(5).keys()].forEach(i => {
      cy.clickCheck('#category-6 > .dropdown-item')
      cy.addProduct(`.products .product:nth-child(${i+1})`, (i+1).toString())
    });
  
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

    cy.get('#content-hook_order_confirmation > .card-block')
      .should("be.visible")
    cy.get('#order-items').should("be.visible")
  })

  it('Check order', () => {
    cy.clickCheck('.account > .hidden-sm-down')
    cy.clickCheck('#history-link > .link-item')
    cy.clickCheck(':nth-child(1) > .order-actions > .view-order-details-link')

    cy.get('#delivery-address > address')
      .should("contain.text", "Jan Kowalski")
  })
})