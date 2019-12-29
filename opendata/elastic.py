import json
import logging
from datetime import datetime

from elasticsearch import Elasticsearch


class Elastic:

    def __init__(self):
        self.logger = logging.getLogger('Elastic class')
        self.logger.setLevel(logging.DEBUG)

        self.elastic = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def save_document(self, index, doc, id_doc, doc_type='opendata'):
        """Save new document in elasticsearch

        Arguments:
            index {str} -- index name
            doc {dict} -- document data
            id_doc {str, float} -- document id

        Keyword Arguments:
            doc_type {str} -- document type (default: {opendata})
        """

        if not doc_type:
            doc_type = index

        try:
            self.elastic.create(index=index, id=id_doc,
                                doc_type=doc_type,
                                body=doc)

        except Exception as error:
            if self.logger:
                self.logger.error("Elasticsearch - Connection refused \n \
                            Error '%s' occured. ", error)


if __name__ == "__main__":
    elastic = Elastic()

    elastic.save_document('test', {'test': 'test'}, id_doc=1)
