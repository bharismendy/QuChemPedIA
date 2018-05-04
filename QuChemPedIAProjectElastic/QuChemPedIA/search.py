from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
connections.create_connection()

def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response