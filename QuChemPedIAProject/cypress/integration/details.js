/* eslint-disable */
/// <reference types="Cypress" />

import molecule1_log from "../fixtures/molecule_1.log"

describe('Molecule details', function () {
  it.only('Show molecule basic information', function () {
    cy.server()

    cy.fixture('molecule_1.json')
    // Stub the response for the molecule details xhr request
    cy.route('GET', '/access/details_json?id_file=iN0gjGoBaHZQCbKmLtmm', 'fixture:molecule_1.json')
      .as('detailsJsonRequest')
    cy.route('GET', '/access/details_author?id_author=1', {"name": "John Smith"})
      .as('detailAuthor1Request')
    cy.route({
      url: '/common_qcpia/static/data_dir/i/N/0/g/j/G/o/B/a/H/Z/Q/C/b/K/m/L/t/m/m/OPT_1557129080642.log.xyz',
      method: 'GET',
      status: 200,
      response: molecule1_log
    })


    // Visit the molecule page, a request that matche the route defined above should be made
    cy.visit('/access/details?id=iN0gjGoBaHZQCbKmLtmm')

    cy.wait(['@detailsJsonRequest',  '@detailAuthor1Request' ])
    //
    // // Molecule Abstract
    // cy.get("[data-testid=molecule_inchi]").contains("1S/C6H5Cl/c7-6-4-2-1-3-5-6/h1-5H")
    // cy.get('[data-testid=molecule_can]').contains("Clc1ccccc1")
    // cy.get('[data-testid=molecule_monoisotopic_mass]').contains("112.00797784")
    // cy.get('[data-testid=molecule_formula]').contains('C6H5Cl')
    // cy.get('[data-testid=molecule_charge]').contains('0')
    // cy.get('[data-testid=molecule_multiplicity]').contains('1')
    //
    // // Computational Details
    // cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-0]').contains('GAMESS ( 1MAY2013 )') // Software
    // cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-1]').contains('DFT') // Method
    // cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-2]').contains('B3LYP')  // Functional
    // cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-3]').contains('6-31G*') // Basis Set name
    // cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-4]').contains('119') // Number of basis set function
    // cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-5]').contains('True') // Closed shell integration
    // cy.get('[data-testid=computationalDetailsTable] [data-testid=data-value-6]').contains('gas') // Solvent
  })

  it('Other molecule', function () {
    cy.server()

    cy.fixture('molecule_2.json')
    // Stub the response for the molecule details xhr request
    cy.route('GET', '/access/details_json?id_file=iN0gjGoBaHZQCbKmLtmm', 'fixture:molecule_2.json')
      .as('detailsJsonRequest')

    cy.route('GET', '/access/details_author?id_author=1', {"name": "John Smith"})
      .as('detailAuthor1Request')

    // Visit the molecule page, a request that matche the route defined above should be made
    cy.visit('/access/details?id=iN0gjGoBaHZQCbKmLtmm')

    cy.wait('@detailsJsonRequest')

    cy.wait('@detailAuthor1Request')
  })

  it('Show message on 404 error', function () {
    cy.server()

    cy.route({
      url: "/access/details_json?id_file=iN0gjGoBaHZQCbKmLtmm",
      method: "GET",
      status: 404,
      response: {}
    }).as('detailsJsonRequest404')

    cy.visit('/access/details?id=iN0gjGoBaHZQCbKmLtmm')

    cy.wait('@detailsJsonRequest404')

    cy.get('[data-testid=details_404]').should('be.visible')
  })
})
