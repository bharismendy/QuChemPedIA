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
        result[str(i)] = []
        result[str(i)].append({
            "id_log": hit.meta.id,
            "InChi": hit.molecule.inchi,
            "cansmiles": hit.molecule.can,
            "smiles": hit.molecule.smi,
            "multiplicity": hit.molecule.multiplicity,
            "ending_energy": hit.results.wavefunction.total_molecular_energy
        })
        i += 1
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
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    q = Q('bool',
          must=[Q('match', molecule__inchi=inchi_value)],
          )
    s = Search().using(es).query(q)[0:20]
    return _search_to_json(search=s.execute())


def search_id(identifier):
    """
    get a unique json file in the database
    :param identifier: integer that correspond to the id in elasticsearch file system
    :return: the content of the json stored in elastic search
    """
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=identifier)
    result = response['_source']
    return result
