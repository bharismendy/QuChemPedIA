/// <reference types="Cypress" />

describe("Molecule details", function () {
  it("Show molecule basic information", function () {
    cy.server();

    cy.fixture("molecule_1.json")
    // Stub the response for the molecule details xhr request
    cy.route('GET', "/details_json?id=iN0gjGoBaHZQCbKmLtmm", 'fixture:molecule_1.json')
      .as("detailsJsonRequest");

    // Visit the molecule page, a request that matche the route defined above should be made
    cy.visit("/details?id=iN0gjGoBaHZQCbKmLtmm");

    cy.wait('@detailsJsonRequest');

    // TODO test rendering
  })
});