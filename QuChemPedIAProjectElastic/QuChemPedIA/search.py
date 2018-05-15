from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import json


def _search_to_json(search):
    """
    function that take a search as parameter and return a json table
    :param search: result of search in elastic search
    :return: json table
    """
    result = {}
    i = 0
    for hit in search:
        try:
            iupac = hit.molecule.iupac
        except Exception as error:
            print(error)
            iupac = "Null"

        try:
            basis_set_name = hit.comp_details.general.basis_set_name
        except Exception as error:
            print(error)
            basis_set_name = "Null"

        try:
            solvatation_method = hit.comp_details.general.solvent_reaction_field
        except Exception as error:
            print(error)
            solvatation_method = "Null"

        try:
            solvent = hit.comp_details.general.solvent
        except Exception as error:
            print(error)
            solvent = "GAS"

        try:
            result[str(i)] = []
            result[str(i)].append({
                "id_log": hit.meta.id,
                "InChi": hit.molecule.inchi,
                "cansmiles": hit.molecule.can,
                "iupac": iupac,  # can be null
                "software": hit.comp_details.general.package,
                "theory": hit.comp_details.general.all_unique_theory[0],
                "functionnal": hit.comp_details.general.functional,
                "basis_set_name": basis_set_name,
                "basis_set_size": hit.comp_details.general.basis_set_size,
                "charge": hit.molecule.charge,
                "multiplicity": hit.molecule.multiplicity,
                "solvatation_method": solvatation_method,
                "solvent": solvent,
                "job_type": "Null",
                "ending_energy": hit.results.wavefunction.total_molecular_energy
            })
            i += 1
        except Exception as error:
            print(error)

    result = str(result).replace("'", "\"")
    json.dumps(result)
    return result


def search_inchi(inchi_value):
    """
    this function search all inchi wich are exactly like the one in parameter
    :param inchi_value: string
    :return: json list of result
    """
    #  connect to elastic search
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          must=[Q('match', molecule__inchi=inchi_value)],
          )
    s = Search().using(es).query(q)[0:20]
    return _search_to_json(search=s.execute())


def search_cid(cid_value):
    """
    this function get all the file for a CID (generally there is only one result)
    :param cid_value: integer, identifier from pubchem database
    :return: a list of json file
    """
    #  connect to elastic search
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          must=[Q('match', molecule__cid=cid_value)],
          )
    s = Search().using(es).query(q)[0:20]
    return _search_to_json(search=s.execute())


def search_iupac(iupac_value):
    """
    this fnction get all iupac that contains the one in parameter
    :param iupac_value: string
    :return: json of result to let the user decide of wich one he want to see
    """
    #  connect to elastic search
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          must=[Q('match', molecule__iupac=iupac_value)],
          )
    s = Search().using(es).query(q)[0:20]
    return _search_to_json(search=s.execute())


def search_formula(formula_value):
    """
    get a compound by it's formula
    :param formula_value: a string equal to a formula
    :return: json list of result
    """
    #  connect to elastic search
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          must=[Q('match', molecule__formula=formula_value)],
          )
    s = Search().using(es).query(q)[0:20]
    return _search_to_json(search=s.execute())


def search_smiles(smiles_value):
    """
    get all compound similar to a smiles
    :param smiles_value: string that contains the smiles to search
    :return: json list of result
    """
    #  connect to elastic search
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          must=[Q('match', molecule__smi=smiles_value)],
          )
    s = Search().using(es).query(q)[0:20]
    return _search_to_json(search=s.execute())

def search_id(id_value):
    """
    get a unique json file in the database
    :param identifier: integer that correspond to the id in elasticsearch file system
    :return: the content of the json stored in elastic search
    """
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=id_value)
    result = response['_source']
    return result
