from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


def search_inchi(inchi_value):
    #  curl -X GET -i http://localhost:9200/quchempedia_index/_search --data '{"query": {"bool": {"must": [{ "match":{ "molecule.smi": "c1ccccc1"}}]}}}' | grep smi
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    q = Q('bool',
          must=[Q('match', molecule__inchi=inchi_value)],
          )
    s = Search().using(es).query(q)[0:20]
    count = s.count()
    print("----------------")
    response = s.execute()
    for hit in s:
        print(hit.molecule.inchi)
    return None


def search_id(identifier):
    ES_HOST = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[ES_HOST])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=identifier)
    res = response['_source']
    return res
