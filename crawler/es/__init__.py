from elasticsearch import Elasticsearch


class ConnectionFailure(Exception):
    pass


def es_check_connection(func):
    """decorator for checking es connection"""
    def _es_check_connection(*args, **kwargs):
        if not args[0].connected:
            raise ConnectionFailure
        func(*args, **kwargs)

    return _es_check_connection


class ESHelper:
    def __init__(self):
        self._es = None

    def connect_es(self):
        self._es = Elasticsearch([{'host': 'localhost', 'port':
                                   9200}])

    @property
    def connected(self):
        return self._es and self._es.ping()
