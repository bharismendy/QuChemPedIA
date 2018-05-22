$(document).ready(function() {

		$.urlParam = function(name){//fonction qui permet de récupérer l'url
		var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
		return results[1] || 0;
        }

        $.ajax({
			//connection au serveur
		   type: 'GET',
		   url: 'http://127.0.0.1:8000/QuChemPedIA/details_json/'+$.urlParam('id'),
		   processData: true,
		   dataType: 'json',
		   success: function(recivedData) {//ce que l'on fait si on a le json
				console.log("Success");
				console.log(results);
				var results;
				if($.urlParam('id')=="demo")
					results = recivedData.data;
				else
					results = recivedData;
					console.log(!results);
				if (!results){
					var html = "<div class='container' style='margin-top:50px;'>";
					html += '<div class="row row404">'
					html += "<h1>404 - We can't find the molecule you're looking for.</h1>";
					html += '</div>'
					html += '<div class="row row404">'
    			html += '<div class="col-xs-4 "><img src='+scientist+'/ style="height:300px;"></div>'
    			html += '<div class="col-xs-4"><img src='+molecule+'/ style="height:300px;"></div>'
					html += '</div>'
					html += '</div>'
					$("#404error").append(html);
				}else{
// autorship categorya
					if(results.metadata){
						var html = "<div class=\"card mt-3\">"
												+"<div class=\"card-header\">"
													+"<h5>Authorship</h5>"
												+"</div>"
												+"<div class=\"container\">";
						if(results.metadata.log_file) html += "<div class=\"row\"><div class=\"col\"><b>Original log file</b></div><div class=\"col\">"+results.metadata.log_file+"</div></div>";
						if(results.metadata.primary_author) html += "<div class=\"row\"><div class=\"col\"><b>Primary author</b></div><div class=\"col\">"+results.metadata.primary_author+"</div></div>";
						if(results.metadata.primary_author_affiliation) html += "<div class=\"row\"><div class=\"col\"><b>Affiliation</b></div><div class=\"col\">"+results.metadata.primary_author_affiliation+"</div></div>";
						html += "</div></div>";
						$("#autorshipMolecule").append(html);
					}

// molecule category
					if(results.molecule){
						var html = "<div class=\"card mt-3\">"
												+"<div class=\"card-header\">"
													+"<h5>Molecule</h5>"
												+"</div>"
												+"<div class=\"container\">";

						//if(cid) html += "<li class=\"list-group-item\"><b>CID :</b>"+cid+"</li>";
						if(results.molecule.iupac) html += "<div class=\"row\"><div class=\"col\"><b>Iupac <span data-placement=\"right\" data-toggle=\"tooltip\" title=\"explicaion info-bulle\" class=\"badge badge-pill monBadge\">?</span></b></div><div class=\"col\">"+results.molecule.iupac+"</div></div>";
						if(results.molecule.inchi) {
							var inchi = (results.molecule.inchi).replace("InChI=","");
							html += "<div class=\"row\"><div class=\"col\"><b>InChI <span data-placement=\"right\" data-toggle=\"tooltip\" title=\"explicaion info-bulle\" class=\"badge badge-pill monBadge\">?</span></b></div><div class=\"col\">"+inchi+"</div></div>";
						}
						if(results.molecule.can) html += "<div class=\"row\"><div class=\"col\"><b>Canonical SMILES <span data-placement=\"right\" data-toggle=\"tooltip\" title=\"explicaion info-bulle\" class=\"badge badge-pill monBadge\">?</span></b></div><div class=\"col\">"+results.molecule.can+"</div></div>";
						if(results.molecule.monoisotopic_mass) html += "<div class=\"row\"><div class=\"col\"><b>Monoisotopic mass</b></div><div class=\"col\">"+results.molecule.monoisotopic_mass+"</div></div>";
						if(results.molecule.formula) html += "<div class=\"row\"><div class=\"col\"><b>Formula <span data-placement=\"right\" data-toggle=\"tooltip\" title=\"explicaion info-bulle\" class=\"badge badge-pill monBadge\">?</span></b></div><div class=\"col\">"+results.molecule.formula+"</div></div>";
						if(results.molecule.charge || (results.molecule.charge == 0)) html += "<div class=\"row\"><div class=\"col\"><b>Charge</b></div><div class=\"col\">"+results.molecule.charge+"</div></div>";
						if(results.molecule.multiplicity || (results.molecule.charge == 0)) html += "<div class=\"row\"><div class=\"col\"><b>Spin multiplicity</b></div><div class=\"col\">"+results.molecule.multiplicity+"</div></div>";
						html += "</div>"
							+"</div>";
						$("#autorshipMolecule").append(html);
					}

					if(results.molecule.can) {
			            let options = {};

			            // Initialize the drawer
			            let smilesDrawer = new SmilesDrawer.Drawer(options);

			            SmilesDrawer.parse(results.molecule.can, function(tree) {
		                    // Draw to the canvas
		                    smilesDrawer.draw(tree, 'canvas', 'light', false);
		                });
					}

// computational details category
					if(results.comp_details){
						var html = "<div class=\"card mt-3\">"
												+"<div class=\"card-header\">"
													+"<h5>Computational details</h5>"
												+"</div>"
												+"<div class=\"container\">";
						if(results.comp_details.general.package) html += "<div class=\"row\"><div class=\"col\"><b>Software </b></div><div class=\"col\">"+results.comp_details.general.package;
						if (results.comp_details.general.package_version) html += " ("+results.comp_details.general.package_version+")";
						html += "</div></div>";
						if (results.comp_details.general.last_theory) html += "<div class=\"row\"><div class=\"col\"><b>Computational method </b></div><div class=\"col\">"+results.comp_details.general.last_theory+"</div></div>";
						if (results.comp_details.general.functional) html += "<div class=\"row\"><div class=\"col\"><b>Functional </b></div><div class=\"col\">"+results.comp_details.general.functional+"</div></div>";
						if (results.comp_details.general.basis_set_name) html += "<div class=\"row\"><div class=\"col\"><b>Basis set name </b></div><div class=\"col\">"+results.comp_details.general.basis_set_name+"</div></div>";

						if (results.comp_details.general.basis_set_size) html += "<div class=\"row\"><div class=\"col\"><b>Number of basis set functions </b></div><div class=\"col\">"+results.comp_details.general.basis_set_size+"</div></div>";
						if (results.comp_details.general.is_closed_shell) html += "<div class=\"row\"><div class=\"col\"><b>Closed shell calculation </b></div><div class=\"col\">"+results.comp_details.general.is_closed_shell+"</div></div>";

						var scf_targets = results.comp_details.general.scf_targets;
						if((scf_targets)&&(scf_targets.length>0)){
							var val = scf_targets[scf_targets.length-1];
							html +="<div class=\"row\"><div class=\"col\"><b>Requested SCF convergence on density </b></div><div class=\"col\">"+val[0]+"</div></div>";
							html +="<div class=\"row\"><div class=\"col\"><b>Threshold on Maximum and RMS Force </b></div><div class=\"col\"> ";
							for(var j=1;j<val.length;j++){
								html += val[j];
								if(j!=(val.length-1))
									html +=", ";
							}
							html += "</div></div>";
						}
						html += "</div>"
							+"</div>";
						$("#ficheMolecule").append(html);
					}


					// results category
					if(results.results){
						var html = "<div class=\"card mt-3\">"
												+"<div class=\"card-header\">"
													+"<h5>Results</h5>"
												+"</div><div id=\"reultsSubList\">";
						html += "</div></div>";
						$("#ficheMolecule").append(html);
					}

					// la partie wavefunction dans results
					if(results.results.wavefunction){
						var html = "<div class=\"container subWavefunction\" class=\"subCard\"><div class=\"container\">";
						if (results.results.wavefunction.total_molecular_energy) html += "<div class=\"row\"><div class=\"col\"><b>Total molecular energy </b></div><div class=\"col\">"+results.results.wavefunction.total_molecular_energy+"</div></div>";
						var homo_indexes = results.results.wavefunction.homo_indexes;
						if ((homo_indexes)&&(homo_indexes.length>0)){
							html += "<div class=\"row\"><div class=\"col\"><b>HOMO number </b></div><div class=\"col\">";
							for(var j=0;j<homo_indexes.length;j++){
								html += (homo_indexes[j]+1);
								if(j!=(homo_indexes.length-1))
									html +=", ";
							}
							html += "</div></div>";
						}
						html += "</div></div>";

						// affichage du tableau des homo energies
						var MO_energies = results.results.wavefunction.MO_energies;
						if ((MO_energies)&&(MO_energies.length>0)){
							html += "<div class=\"container subWavefunction\" align=center><b>Calculated energies for the frontier molecular orbitals (in eV)</b>";
							html += "<table class=\"tableauWavefunction\" id=\"tableMO_energies\">";
							html += "<tr><td>HOMO-1</td><td>HOMO</td><td>LUMO</td><td>LUMO+1</td></tr>";
							for(var j=0;j<homo_indexes.length;j++){
								html += "<tr><td>"+MO_energies[j][homo_indexes[j]-1].toFixed(2)+"</td><td>"+MO_energies[j][homo_indexes[j]].toFixed(2)+"</td><td>"+MO_energies[j][homo_indexes[j]+1].toFixed(2)+"</td><td>"+MO_energies[j][homo_indexes[j]+2].toFixed(2)+"</td></tr>";
							}
							html += "</table></div>";
						}

						html += "<div class=\"container subWavefunction\" align=center><b>Atom numbering scheme.</b></div>";
						
						var Symbol = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Uuq","Uup","Uuh","Uus","Uuo"];

						// affichage du tableau des Mulliken atomic
						var Mulliken_partial_charges = results.results.wavefunction.Mulliken_partial_charges;
						if ((Mulliken_partial_charges)&&(Mulliken_partial_charges.length>0)){

							var atoms_Z = results.molecule.atoms_Z;
							var indices = new Array();
							for(var j=0;j<Mulliken_partial_charges.length;j++)
								indices[j]=j;

							//trier le tableau des enérgies
							for(var j=0;j<Mulliken_partial_charges.length;j++){
								for(var h=j;h<(Mulliken_partial_charges.length -1);h++){
									if(Mulliken_partial_charges[h]<Mulliken_partial_charges[j]){
										var temp = Mulliken_partial_charges[h];
										var temp0 = indices[h];
										var temp1 = atoms_Z[h];

										Mulliken_partial_charges[h] = Mulliken_partial_charges[j];
										indices[h] = indices[j];
										atoms_Z[h] = atoms_Z[j];
										Mulliken_partial_charges[j] = temp;
										indices[j] = temp0;
										atoms_Z[j] = temp1;
									}
								}
							}

							html += "<div class=\"container subWavefunction\" align=center><b>Most intense Mulliken atomic charges (|q| > 0.1 e)</b>";
							html += "<table class=\"tableauWavefunction\" id=\"tableMulliken_partial_charges\">";
							html += "<tr><td>Atom</td><td>number</td><td>Mulliken partial charges</td></tr>";

							for(var j=0;j<Mulliken_partial_charges.length;j++){
								html += "<tr><td>"+Symbol[atoms_Z[j]]+"</td><td>"+indices[j]+"</td><td>"+Mulliken_partial_charges[j].toFixed(3)+"</td></tr>";
							}
							html += "</table></div>";

						}


						$("#reultsSubList").append(html);
					}

					// la partie geometry
					if(results.results.geometry){
						var html = "<div class=\"container\" class=\"subCard\"><h5 class=\"card-title subTitle\">Geometry</h5><div class=\"container\">";
						if (results.results.geometry.nuclear_repulsion_energy_from_xyz) html += "<div class=\"row\"><div class=\"col\"><b>Nuclear repulsion energy in atomic units </b></div><div class=\"col\">"+results.results.geometry.nuclear_repulsion_energy_from_xyz+"</div></div>";
						if (results.results.geometry.OPT_DONE) html += "<div class=\"row\"><div class=\"col\"><b>Is it a result of a geometry optimization? </b></div><div class=\"col\">"+results.results.geometry.OPT_DONE+"</div></div>";
						html += "</div></div>";
						$("#reultsSubList").append(html);
					}

					// la partie excited_states
					if(results.results.excited_states){
						var html = "<div class=\"container\" class=\"subCard\"><h5 class=\"card-title subTitle\">Excited states</h5><div class=\"container\">";

						html += "</div></div>";
						$("#reultsSubList").append(html);
					}
				}

				$('[data-toggle="tooltip"]').tooltip();
			}
		});

});
