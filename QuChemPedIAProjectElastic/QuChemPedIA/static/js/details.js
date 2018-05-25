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
				var results;
				var ancienneCouleure;
				if($.urlParam('id')=="demo")
					results = recivedData.data;
				else
					results = recivedData;
					//console.log(results);
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
							var inch = results.molecule.inchi;
							var inchi;
							if($.isArray(inch)) inchi = inch[0].replace("InChI=","");
							else inchi = inch.replace("InChI=","");
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
					
// associated calculations category
					if(results.metadata) {
						var html1 = "<div class=\"card mt-3\">"
													+"<div class=\"card-header\">"
														+"<h5>Associated calculations</h5>"
													+"</div>"
													+"<div class=\"container\">";

						html1 += "<div class=\"row\"><div class=\"col\"><b>Job type</b></div><div class=\"col\"><b>Author</b></div><div class=\"col\"><b>Description</b></div><div class=\"col\"></div></div>";
						html1 += "<div class=\"row mySiblingsRow\"><div class=\"col my-auto\">"+recivedData.job_type+"</div><div class=\"col my-auto\">"+(results.metadata.primary_author?results.metadata.primary_author:"N/A")+"</div><div class=\"col my-auto\">N/A</div><div class=\"col my-auto\"><button type=\"button\" style=\"background-color:transparent\" id=\"opt\" class=\"btn btn-primary-outline\"><span class=\"fa fa-file-text\" aria-hidden=\"true\"></span></button></div></div>";
						$.each(recivedData.siblings, function(key,val) {
							html1 += "<div class=\"row mySiblingsRow\"><div class=\"col my-auto\">"+val.data.metadata.log_file+"</div><div class=\"col my-auto\">"+(val.data.metadata.primary_author?val.data.metadata.primary_author:"N/A")+"</div><div class=\"col my-auto\">N/A</div><div class=\"col my-auto\"><button type=\"button\" style=\"background-color:transparent\" id="+key+" class=\"btn btn-primary-outline myButton\"><span class=\"fa fa-file-text\" aria-hidden=\"true\"></span></button></div></div>";
							if(val.job_type=="TD") {
								$.each(val.siblings, function(key2,val2) {
									html1 += "<div class=\"row mySiblingsRow\"><div class=\"col my-auto\">&nbsp;&nbsp;&nbsp;<i class=\"fa fa-angle-right\"></i> "+val2.data.metadata.log_file+"</div><div class=\"col my-auto\">"+(val2.data.metadata.primary_author?val2.data.metadata.primary_author:"N/A")+"</div><div class=\"col my-auto\">N/A</div><div class=\"col my-auto\"><button type=\"button\" style=\"background-color:transparent\" id="+key+"_"+key2+" class=\"btn btn-primary-outline myButton\"><span class=\"fa fa-file-text\" aria-hidden=\"true\"></span></button></div></div>";
								});
							}
						});
						html1 += "</div></div>";
						$("#associatedCalculations").append(html1);
					}
					$("#opt").click(function() {
						$("#"+this.id).parent().parent().parent().children().css( "background-color", "white" );
						$("#"+this.id).parent().parent().css( "background-color", "#e5e7e9" );
						ancienneCouleure = "#e5e7e9";
						computationalDetailsEtResults(results);
					});
					$(".myButton").click(function() {
						var arrayKeys = this.id.split("_");
						$("#"+this.id).parent().parent().parent().children().css( "background-color", "white" );
						$("#"+this.id).parent().parent().css( "background-color", "#e5e7e9" );
						ancienneCouleure = "#e5e7e9";
						if(arrayKeys.length==1) {
							computationalDetailsEtResults(recivedData.siblings[parseInt(this.id)].data);
						} else {
							computationalDetailsEtResults(recivedData.siblings[arrayKeys[0]].siblings[arrayKeys[1]].data);
						}
					});
				}
				
				//$(".mySiblingsRow").click(function(){ $(this).find("button").click(); });
				
				computationalDetailsEtResults(results);
				$("#opt").parent().parent().css( "background-color", "#e5e7e9" );
				$('[data-toggle="tooltip"]').tooltip();
				$(".mySiblingsRow").hover(function(){ancienneCouleure = $(this).css( "background-color");$(this).css( "background-color", "#e5e7e9" );},function(){$(this).css( "background-color", ancienneCouleure );});
			},
			error: function() {
				console.log("ERROR");
			},
			
		});
		
		
		function computationalDetailsEtResults(results){			
					var htm = "";						
					var Symbol = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Uuq","Uup","Uuh","Uus","Uuo"];

					
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
						htm += html;						
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
						htm += html;
					}


// results category
					if(results.results){
						var html = "<div class=\"card mt-3\">"
												+"<div class=\"card-header\">"
													+"<h5>Results</h5>"
												+"</div><div id=\"reultsSubList\">";
						html += "</div></div>";
						htm += html;
						$("#ficheMolecule").empty();
						$("#ficheMolecule").append(htm);
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

		// affichage du tableau des Mulliken atomic
						var Mulliken_partial_charges = results.results.wavefunction.Mulliken_partial_charges;
						if ((Mulliken_partial_charges)&&(Mulliken_partial_charges.length>0)){

							var atoms_Z = results.molecule.atoms_Z;
							var atom_z = new Array();
							for(var j=0;j<atoms_Z.length;j++)
								atom_z[j]=atoms_Z[j];
								
							var indices = new Array();
							for(var j=0;j<Mulliken_partial_charges.length;j++)
								indices[j]=j;
								
							var mulliken_partial_charges = new Array();
							for(var j=0;j<Mulliken_partial_charges.length;j++)
								mulliken_partial_charges[j]=Mulliken_partial_charges[j];

				//trier le tableau des enérgies
							for(var j=0;j<mulliken_partial_charges.length;j++){
								for(var h=j;h<(mulliken_partial_charges.length -1);h++){
									if(mulliken_partial_charges[h]<mulliken_partial_charges[j]){
										var temp = mulliken_partial_charges[h];
										var temp0 = indices[h];
										var temp1 = atom_z[h];

										mulliken_partial_charges[h] = mulliken_partial_charges[j];
										indices[h] = indices[j];
										atom_z[h] = atom_z[j];
										mulliken_partial_charges[j] = temp;
										indices[j] = temp0;
										atom_z[j] = temp1;
									}
								}
							}

							html += "<div class=\"container subWavefunction\" align=center><b>Most intense Mulliken atomic charges (|q| > 0.1 e)</b>";
							html += "<table class=\"tableauWavefunction\" id=\"tableMulliken_partial_charges\">";
							html += "<tr><td>Atom</td><td>number</td><td>Mulliken partial charges</td></tr>";

							for(var j=0;j<mulliken_partial_charges.length;j++){
								html += "<tr><td>"+Symbol[atom_z[j]-1]+"</td><td>"+indices[j]+"</td><td>"+mulliken_partial_charges[j].toFixed(3)+"</td></tr>";
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
						
						html += "</br><p>This calculation is the result of a geometry optimization process.</p>";
						
			// dessin du tableau des convergence
			// cas ou le logiciel est "Gaussian"
						if(results.comp_details.general.package && (results.comp_details.general.package=="Gaussian")){
							if(results.comp_details.geometry.geometric_targets){
								var geometric_targets = results.comp_details.geometry.geometric_targets;
								var geometric_values = results.results.geometry.geometric_values[results.results.geometry.geometric_values.length -1 ];
								var titreCols = ["Maximum Force","RMS Force","Maximum Displacement","RMS Displacement"];
								html += "<div class=\"container subConvergence\" align=center><b>Geometry optimization convergence criteria</b>";
								html += "<table class=\"tableauConvergence\" id=\"geometric_targets\">";
								html += "<tr><td></td><td>Value</td><td>Threshold</td></tr>";
								for(var i=0;i<geometric_targets.length && i< titreCols.length;i++){
									html += "<tr><td class=\"cellulTitre\">"+titreCols[i]+"</td><td>"+geometric_values[i]+"</td><td>"+geometric_targets[i]+"</td></tr>";
								}
								html += "</table></div>";
							}
						}// else if "un autre logiciel"

				
						
			// dessin du tableau Cartesian atomic coordinates
						if(results.results.geometry.elements_3D_coords_converged){
							var elements_3D_coords_converged = results.results.geometry.elements_3D_coords_converged;
							var atoms_Z = results.molecule.atoms_Z;
							html += "<div class=\"container subCartesian\" align=center><b>Cartesian atomic coordinates in Angstroms</b>";
							html += "<table class=\"tableauCartesian\" id=\"elements_3D_coords_converged\">";
							html += "<tr><td>Atom</td><td>X</td><td>Y</td><td>Z</td></tr>";
							for(var i=0;i<elements_3D_coords_converged.length;i+=3){
								html += "<tr><td>"+Symbol[atoms_Z[i/3]-1]+"</td><td>"+elements_3D_coords_converged[i]+"</td><td>"+elements_3D_coords_converged[i+1]+"</td><td>"+elements_3D_coords_converged[i+2]+"</td></tr>";
							}
							html += "</table></div>";
						}
						
						
						html += "</div></div>";
						$("#reultsSubList").append(html);
					}
					
		// la partie Thermochemistry and normal modes
					if(results.results.freq){
						var html = "<div class=\"container\" class=\"subCard\"><h5 class=\"card-title subTitle\">Thermochemistry and normal modes</h5><div class=\"container\">";
						if (results.results.freq.zero_point_energy) html += "<div class=\"row\"><div class=\"col\"><b>Sum of electronic and zero-point energy in Hartrees </b></div><div class=\"col\">"+results.results.freq.zero_point_energy+"</div></div>";
						if (results.results.freq.electronic_thermal_energy) html += "<div class=\"row\"><div class=\"col\"><b>Sum of electronic and thermal at 298.150000 K energies in atomic units </b></div><div class=\"col\">"+results.results.freq.electronic_thermal_energy+"</div></div>";
						
						
						if (results.results.freq.entropy) html += "<div class=\"row\"><div class=\"col\"><b>Entropy at 298.150000 K in atomic units </b></div><div class=\"col\">"+results.results.freq.entropy.toFixed(15)+"</div></div>";
						if (results.results.freq.enthalpy) html += "<div class=\"row\"><div class=\"col\"><b>Enthalpy at 298.150000 K in atomic units </b></div><div class=\"col\">"+results.results.freq.enthalpy+"</div></div>";
						if (results.results.freq.free_energy) html += "<div class=\"row\"><div class=\"col\"><b>Gibbs free energy at 298.150000 K in atomic units </b></div><div class=\"col\">"+results.results.freq.free_energy+"</div></div>";
						
						html += "</div></div>";
						
						
				// dessin du tableau des vibrations
						if(results.results.freq.vibrational_int){
							var vibrational_freq = results.results.freq.vibrational_freq;
							var vibrational_int = results.results.freq.vibrational_int;
							var vibrational_sym = results.results.freq.vibrational_sym;
							html += "<div class=\"container subVibrations\" align=center><b>Table of the most intense molecular vibrations (> 20 km/mol) (14)</b>";
							html += "<table class=\"tableauVibrations\" id=\"vibrational_int\">";
							html += "<tr><td>Frequencies</td><td>Intensity</td><td>Symmetry</td></tr>";
							for(var i=0;i<vibrational_int.length;i+=3){
								if(vibrational_int[i] > 20)
									html += "<tr><td>"+vibrational_freq[i]+"</td><td>"+vibrational_int[i]+"</td><td>"+vibrational_sym[i]+"</td></tr>";
							}
							html += "</table></div>";
						}
						
						
						$("#reultsSubList").append(html);
					}
					

		// la partie excited_states
					if(results.results.excited_states){
						var html = "<div class=\"container\" class=\"subCard\"><h5 class=\"card-title subTitle\">Excited states</h5><div class=\"container\">";

						html += "</div></div>";
						$("#reultsSubList").append(html);
					}	
						
		}
		 

});


















