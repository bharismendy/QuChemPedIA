from elasticsearch import Elasticsearch
from QuChemPedIA.models.json2obj import json2obj

def search_inchi(inchi_value):
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    # response = es.get(index="quchempedia_index", doc_type="log_file", id=5)
    # print(response)
    response2 = es.search(index="quchempedia_index", body={"query": {"match": {"inchi": inchi_value}}})
    print(response2)
    return None


def search_id(id):
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=id)
    res = response['_source']
    return res
