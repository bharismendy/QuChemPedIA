from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from QuChemPedIA.models.QueryModel import Query
from .search import QuChemPedIAIndex
connections.create_connection()


class QuChemPedIAIndex(DocType):
    author = Text()
    posted_date = Date()
    title = Text()
    text = Text()

    class Meta:
        index = 'QuChemPedIA-index'


def bulk_indexing():
    QuChemPedIAIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in Query.objects.all().iterator()))