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

				
				
			}
		});
	
	
	/*
	results = $("<div>").html(results).html();
	results = results.substring(1,results.length-1);
	results = jQuery.parseJSON(results);
	
	//console.log(results);
	//console.log(Object.keys(results).length);
	
	
	var keys = Object.keys(results);
	var values = Object.values(results);	
	for(var i=0;i<keys.length;i++){
		console.log(keys[i]);
		
		var keys2 = Object.keys(values[i]);
		var values2 = Object.values(values[i]);
		for(var j=0;j<keys2.length;j++){
			console.log("\t"+keys2[j]);
			var html = "<li class=\"list-group-item list-group-item-light\">"+keys2[j]+"</li>";
			$("#panneauLateralList").append(html);
			
			
			var html2 = "<div class=\"card border-dark mb-3\" style=\"max-width: 18rem;\">"
			  +"<div class=\"card-header\">Header</div>"
			  +"<div class=\"card-body text-dark\">"
				+"<h5 class=\"card-title\">Dark card title</h5>"
				+"<p class=\"card-text\"></p>"
			  +"</div>"
			+"</div>";
		}
		
	}
		
		
		
		
		
		
	var inchi = results.molecule.inchi;
	var formula = results.molecule.formula;
	console.log(inchi);
	console.log(formula);
*/

});
