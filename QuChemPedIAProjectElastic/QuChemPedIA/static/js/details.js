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
		   success: function(results) {//ce que l'on fait si on a le json
				console.log("Success");
				//console.log(results);
				
				// autorship category
				if(results.metadata){
					var html = "<div class=\"card mt-3\">"
											+"<div class=\"card-header\">"
												+"<h5>Authorship</h5>"
											+"</div>"
											+"<ul class=\"list-group list-group-flush\">";
					if(results.metadata.log_file) html += "<li class=\"list-group-item\"><b>Original log file :</b>"+results.metadata.log_file+"</li>";
					if(results.metadata.primary_author) html += "<li class=\"list-group-item\"><b>Primary author :</b>"+results.metadata.primary_author+"</li>";
					if(results.metadata.primary_author_affiliation) html += "<li class=\"list-group-item\"><b>Affiliation :</b>"+results.metadata.primary_author_affiliation+"</li>";
					html += "</ul>"
						+"</div>";
					$("#autorshipMolecule").append(html);
				}
								
				// molecule category
				if(results.molecule){
					var html = "<div class=\"card mt-3\">"
											+"<div class=\"card-header\">"
												+"<h5>Molecule</h5>"
											+"</div>"
											+"<ul class=\"list-group list-group-flush\">";
					//if(cid) html += "<li class=\"list-group-item\"><b>CID :</b>"+cid+"</li>";
					if(results.molecule.iupac) html += "<li class=\"list-group-item\"><b>Iupac :</b>"+results.molecule.iupac+"</li>";
					if(results.molecule.inchi) html += "<li class=\"list-group-item\"><b>InChI :</b>"+results.molecule.inchi+"</li>";
					if(results.molecule.can) html += "<li class=\"list-group-item\"><b>CanSMILES :</b>"+results.molecule.can+"</li>";
					if(results.molecule.monoisotopic_mass) html += "<li class=\"list-group-item\"><b>Monoisotopic mass :</b>"+results.molecule.monoisotopic_mass+"</li>";
					if(results.molecule.formula) html += "<li class=\"list-group-item\"><b>Formula :</b>"+results.molecule.formula+"</li>";
					if(results.molecule.charge || (results.molecule.charge == 0)) html += "<li class=\"list-group-item\"><b>Charge :</b>"+results.molecule.charge+"</li>";
					if(results.molecule.multiplicity || (results.molecule.charge == 0)) html += "<li class=\"list-group-item\"><b>Spin multiplicity :</b>"+results.molecule.multiplicity+"</li>";
					html += "</ul>"
						+"</div>";
					$("#autorshipMolecule").append(html);
				}
				
				// computational details category
				if(results.comp_details){
					var html = "<div class=\"card mt-3\">"
											+"<div class=\"card-header\">"
												+"<h5>Computational details</h5>"
											+"</div>"
											+"<div class=\"container\">";
					if(results.comp_details.general.package) html += "<div class=\"row\"><div class=\"col\"><b>Software </b></div><div class=\"col\">"+results.comp_details.general.package;
					if (results.comp_details.general.package_version) html += "("+results.comp_details.general.package_version+")";
					html += "</div></div>";
					if (results.comp_details.general.last_theory) html += "<div class=\"row\"><div class=\"col\"><b>Computational method </b></div><div class=\"col\">"+results.comp_details.general.last_theory+"</div></div>";
					if (results.comp_details.general.functional) html += "<div class=\"row\"><div class=\"col\"><b>Functional </b></div><div class=\"col\">"+results.comp_details.general.functional+"</div></div>";
					if (results.comp_details.general.basis_set_name) html += "<div class=\"row\"><div class=\"col\"><b>Basis set name </b></div><div class=\"col\">"+results.comp_details.general.basis_set_name+"</div></div>";
				
					if (results.comp_details.general.basis_set_size) html += "<div class=\"row\"><div class=\"col\"><b>Number of basis set functions </b></div><div class=\"col\">"+results.comp_details.general.basis_set_size+"</div></div>";
					if (results.comp_details.general.is_closed_shell) html += "<div class=\"row\"><div class=\"col\"><b>Requested SCF convergence on density </b></div><div class=\"col\">"+results.comp_details.general.is_closed_shell+"</div></div>";
					html +="<div class=\"row\"><div class=\"col\"><b>Requested SCF convergence on density </b></div><div class=\"col\"> XXXXX </div></div>";
					html +="<div class=\"row\"><div class=\"col\"><b>Threshold on Maximum and RMS Force </b></div><div class=\"col\"> XXXXX </div></div>";
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
				
				if(results.results.wavefunction){
					var html = "<div class=\"container\" class=\"subCard\"><h5 class=\"card-title subTitle\">Wavefunction</h5><div class=\"container\">";
					if (results.results.wavefunction.total_molecular_energy) html += "<div class=\"row\"><div class=\"col\"><b>Total molecular energy </b></div><div class=\"col\">"+results.results.wavefunction.total_molecular_energy+"</div></div>";
					if (results.results.wavefunction.MO_number) html += "<div class=\"row\"><div class=\"col\"><b>HOMO number </b></div><div class=\"col\">"+results.results.wavefunction.MO_number+"</div></div>";
					html += "</div></div>";
					$("#reultsSubList").append(html);
				}
				
				if(results.results.geometry){
					var html = "<div class=\"container\" class=\"subCard\"><h5 class=\"card-title subTitle\">Geometry</h5><div class=\"container\">";
					if (results.results.geometry.nuclear_repulsion_energy_from_xyz) html += "<div class=\"row\"><div class=\"col\"><b>Nuclear repulsion energy in atomic units </b></div><div class=\"col\">"+results.results.geometry.nuclear_repulsion_energy_from_xyz+"</div></div>";
					if (results.results.geometry.OPT_DONE) html += "<div class=\"row\"><div class=\"col\"><b>Nuclear repulsion energy in atomic units </b></div><div class=\"col\">"+results.results.geometry.OPT_DONE+"</div></div>";
					html += "</div></div>";
					$("#reultsSubList").append(html);
				}
				
				if(results.results.excited_states){
					var html = "<div class=\"container\" class=\"subCard\"><h5 class=\"card-title subTitle\">Excited states</h5><div class=\"container\">";
					
					html += "</div></div>";
					$("#reultsSubList").append(html);
				}
				
			}
		});

});
