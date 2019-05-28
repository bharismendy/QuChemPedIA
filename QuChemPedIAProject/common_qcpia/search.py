from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import json
from django.conf import settings
from itertools import chain


def find(key, dictionary):
    """
    function to find a list of all value set for a key in a json
    :param key: key where value are set
    :param dictionary: json to explore
    :return: a list of result
    """
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find(key, d):
                        yield result


def _get_job_type(file_to_analyze, name_key='job_type'):
    """
    function that return a list of job_type from a document
    :param file_to_analyze: json to analyze
    :param name_key: name of the job type
    :return: array of job_type
    """
    if not type(file_to_analyze) is dict:
        file_to_analyze = file_to_analyze.to_dict()
    result = list(set(chain(*find(name_key, file_to_analyze))))
    return result


def _search_to_json(search, nbresult):
    """
    function that take a search as parameter and return a json table
    :param search: result of search in elastic search
    ;:param nbresult : number of result
    :return: json table
    """
    result = {}
    i = 0
    for hit in search:
        try:
            iupac = hit.data.molecule.iupac
        except:
            iupac = "Null"

        try:
            basis_set_name = hit.data.comp_details.general.basis_set_name
        except Exception as error:
            basis_set_name = "Null"

        try:
            solvatation_method = hit.data.comp_details.general.solvent_reaction_field
        except Exception as error:
            solvatation_method = "Null"

        try:
            solvent = hit.data.comp_details.general.solvent
        except Exception as error:
            solvent = "GAS"

        try:
            result[str(i)] = []
            result[str(i)].append({
                "id_log": hit.meta.id,
                "InChi": hit.data.molecule.inchi,
                "cansmiles": hit.data.molecule.can,
                "iupac": iupac,  # can be null
                "software": hit.data.comp_details.general.package,
                "theory": hit.data.comp_details.general.all_unique_theory[0],
                "functionnal": hit.data.comp_details.general.functional,
                "basis_set_name": basis_set_name,
                "formula": hit.data.molecule.formula,
                "basis_set_size": hit.data.comp_details.general.basis_set_size,
                "charge": hit.data.molecule.charge,
                "multiplicity": hit.data.molecule.multiplicity,
                "solvatation_method": solvatation_method,
                "solvent": solvent,
                "job_type": _get_job_type(hit),
                "ending_energy": hit.data.results.wavefunction.total_molecular_energy
            })
            i += 1
        except Exception as error:
            print(error)
    result['nbresult'] = nbresult
    result = str(result).replace("'", "\"")
    json.dumps(result)
    return result


def search_inchi(inchi_value, page, nbrpp):
    """
    this function search all inchi wich are exactly like the one in parameter
    :param inchi_value: string
    :param page: number of displayed page of result
    :param nbrpp: number of result in a page
    :return: json list of result
    """
    #  connect to elastic search
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          should=[Q('match', data__molecule__inchi=inchi_value)],
          )
    s = Search().using(es).query(q)[nbrpp*page-nbrpp:(nbrpp*page)-1]

    return _search_to_json(search=s.execute(), nbresult=s.count())


def search_id_user(id_user, page, nbrpp):
    """
     this function get all the file were the user contribute
     :param id_user: integer, identifier of the user
     :param page: number of displayed page of result
     :param nbrpp: number of result in a page
     :return: a list of json file
     """
    #  connect to elastic search
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          should=[Q('match', data__metadata__id_user=id_user)],
          )
    s = Search().using(es).query(q)[nbrpp * page - nbrpp:(nbrpp * page) - 1]
    return _search_to_json(search=s.execute(), nbresult=s.count())


def search_cid(cid_value, page, nbrpp):
    """
    this function get all the file for a CID (generally there is only one result)
    :param cid_value: integer, identifier from pubchem database
    :param page: number of displayed page of result
    :param nbrpp: number of result in a page
    :return: a list of json file
    """
    #  connect to elastic search
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          should=[Q('match', data__molecule__cid=cid_value)],
          )
    s = Search().using(es).query(q)[nbrpp*page-nbrpp:(nbrpp*page)-1]
    return _search_to_json(search=s.execute(), nbresult=s.count())


def search_iupac(iupac_value, page, nbrpp):
    """
    this fnction get all iupac that contains the one in parameter
    :param iupac_value: string
    :param page: number of displayed page of result
    :param nbrpp: number of result in a page
    :return: json of result to let the user decide of wich one he want to see
    """
    #  connect to elastic search
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          should=[Q('match', data__molecule__iupac=iupac_value)],
          )
    s = Search().using(es).query(q)[nbrpp*page-nbrpp:(nbrpp*page)-1]
    return _search_to_json(search=s.execute(), nbresult=s.count())


def search_formula(formula_value, page, nbrpp):
    """
    get a compound by it's formula
    :param formula_value: a string equal to a formula
    :param page: number of displayed page of result
    :param nbrpp: number of result in a page
    :return: json list of result
    """
    #  connect to elastic search
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          should=[Q('match', data__molecule__formula=formula_value)],
          )
    s = Search().using(es).query(q)[nbrpp*page-nbrpp:(nbrpp*page)-1]
    return _search_to_json(search=s.execute(), nbresult=s.count())


def search_smiles(smiles_value, page, nbrpp):
    """
    get all compound similar to a smiles
    :param smiles_value: string that contains the smiles to search
    :param page: number of displayed page of result
    :param nbrpp: number of result in a page
    :return: json list of result
    """
    #  connect to elastic search
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    q = Q('bool',
          should=[Q('match', data__molecule__smi=smiles_value)],
          )
    s = Search().using(es).query(q)[nbrpp*page-nbrpp:(nbrpp*page)-1]
    return _search_to_json(search=s.execute(), nbresult=s.count())


def search_id(id_value):
    """
    get a unique json file in the database
    :param id_value: string that correspond to the id in elasticsearch file system
    :return: the content of the json stored in elastic search
    """
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=id_value)
    result = response['_source']
    return result

