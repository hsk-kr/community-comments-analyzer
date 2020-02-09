from elasticsearch import Elasticsearch
from . import ESHelper, es_check_connection


class DogdripESHelper(ESHelper):
    # constants
    INDEX_NAME = "dogdrip"
    COMMENTS_TYPE_NAME = "comments"

    def __init__(self):
        super()
        self.connect_es()
        self.__create_comments_index()

    @es_check_connection
    def __create_comments_index(self):
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "tokenizer": {
                        "korean_tokenizer": {
                            "type": "nori_tokenizer"
                        }
                    },
                    "analyzer": {
                        "korean": {
                            "type": "custom",
                            "tokenizer": "korean_tokenizer"
                        }
                    }
                }
            },
            "mappings": {
                DogdripESHelper.COMMENTS_TYPE_NAME: {
                    "properties": {
                        "comments": {
                            "type": "nested",
                            "properties": {
                                "nickname": {
                                    "type": "keyword"
                                },
                                "content": {
                                    "type": "text",
                                    "analyzer": "korean"
                                },
                                "like_votes": {
                                    "type": "integer"
                                },
                                "date": {
                                    "type": "date"
                                }
                            }
                        }
                    }
                }
            }
        }

        if not self._es.indices.exists(DogdripESHelper.INDEX_NAME):
            # Ignore "Index already Exist" error.
            # pylint: disable=unexpected-keyword-arg
            test = self._es.indices.create(
                index=DogdripESHelper.INDEX_NAME, include_type_name=True, ignore=400, body=settings)
            print(test)

    @es_check_connection
    def index_comments(self, postnum, comments):
        self._es.index(index=DogdripESHelper.INDEX_NAME,
                       doc_type=DogdripESHelper.COMMENTS_TYPE_NAME, id=postnum, body={"comments": comments})

    @es_check_connection
    def delete_comments(self, postnum):
        self._es.delete(index=DogdripESHelper.INDEX_NAME,
                        doc_type=DogdripESHelper.COMMENTS_TYPE_NAME, id=postnum)
