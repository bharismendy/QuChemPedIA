from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import json


def search_inchi(inchi_value):
    #  connect to elastic search
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    q = Q('bool',
          must=[Q('match', molecule__inchi=inchi_value)],
          )
    s = Search().using(es).query(q)[0:20]
    response = s.execute()
    # create a json witch going to return data from extracted json
    result = {}
    i = 0
    for hit in s:
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


def search_id(identifier):
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=identifier)
    res = response['_source']
    return res
