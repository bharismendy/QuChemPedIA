/* eslint-disable */
/// <reference types="Cypress" />

describe('Molecule details', function () {
  it('Show molecule basic information', function () {
    cy.server()

    cy.fixture('molecule_1.json')
    // Stub the response for the molecule details xhr request
    cy.route('GET', '/access/details_json?id_file=iN0gjGoBaHZQCbKmLtmm', 'fixture:molecule_1.json')
      .as('detailsJsonRequest')

    // Visit the molecule page, a request that matche the route defined above should be made
    cy.visit('/access/details?id=iN0gjGoBaHZQCbKmLtmm')

    cy.wait('@detailsJsonRequest')

    // Molecule Abstract
    cy.get("[data-testid=molecule_inchi]").contains("1S/C6H5Cl/c7-6-4-2-1-3-5-6/h1-5H")
    cy.get('[data-testid=molecule_can]').contains("Clc1ccccc1")
    cy.get('[data-testid=molecule_monoisotopic_mass]').contains("112.00797784")
    cy.get('[data-testid=molecule_formula]').contains('C6H5Cl')
    cy.get('[data-testid=molecule_charge]').contains('0')
    cy.get('[data-testid=molecule_multiplicity]').contains('1')

    // Computational Details
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-0]').contains('Gaussian ( 09revisionD.01 )') // Software
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-1]').contains('DFT') // Method
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-2]').contains('B3LYP')  // Functional
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-3]').contains('6-31G(d)') // Basis Set name
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-4]').contains('119') // Number of basis set function
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-5]').contains('True') // Closed shell integration
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-6]').contains('Ultrafine') // Integration grid
    cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-7]').contains('Gas') // Solvent
  })
})
