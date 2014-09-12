# -*- coding: utf-8 -*-

from arangodb.api import Client, Document
from arangodb.query.utils.document import create_document_from_result_dict


class QueryFilterStatement(object):
    EQUAL_OPERATOR = '=='

    def __init__(self, collection, attribute, operator, value):
        """
        """

        self.collection = collection
        self.attribute = attribute
        self.operator = operator
        self.value = value


class Query(object):
    SORTING_ASC = 'ASC'
    SORTING_DESC = 'DESC'

    def __init__(self):
        """
        """

        self.collections = []
        self.filters = []

        self.start = -1
        self.count = -1

        self.sorting = []

    def append_collection(self, collection_name):
        """
        """

        self.collections.append(collection_name)

        return self

    def filter(self, **kwargs):

        for key, value in kwargs.iteritems():

            splitted_filter = key.split('__')

            if len(splitted_filter) is 1:

                self.filters.append(
                    QueryFilterStatement(
                        collection=self.collections[-1],
                        attribute=key,
                        operator=QueryFilterStatement.EQUAL_OPERATOR,
                        value=value,
                    )
                )

            else:

                self.filters.append(
                    QueryFilterStatement(
                        collection=splitted_filter[0],
                        attribute=splitted_filter[1],
                        operator=QueryFilterStatement.EQUAL_OPERATOR,
                        value=value,
                    )
                )

        return self

    def limit(self, count, start=-1):
        self.start = start
        self.count = count

    def order_by(self, field, order=None, collection=None):

        if order is None:
            order = self.SORTING_ASC

        self.sorting.append({
            'field': field,
            'order': order,
            'collection': collection,
        })

    def execute(self):
        """
        """

        query_data = ''

        for collection in self.collections:
            query_data += ' FOR %s in %s' % (
                self._get_collection_ident(collection),
                collection
            )

        for filter_statement in self.filters:

            if isinstance(filter_statement.value, basestring):
                query_data += ' FILTER %s.%s %s "%s"' % (
                    self._get_collection_ident(filter_statement.collection),
                    filter_statement.attribute,
                    filter_statement.operator,
                    filter_statement.value,
                )
            else:
                query_data += ' FILTER %s.%s %s %s' % (
                    self._get_collection_ident(filter_statement.collection),
                    filter_statement.attribute,
                    filter_statement.operator,
                    filter_statement.value,
                )

        is_first = True

        for sorting_entry in self.sorting:

            if is_first:
                query_data += ' SORT '

            if sorting_entry['field'] is not None:

                if not is_first:
                    query_data += ', '

                if sorting_entry['collection'] is not None:
                    query_data += '%s.%s %s' % (
                        self._get_collection_ident(sorting_entry['collection']),
                        sorting_entry['field'],
                        sorting_entry['order'],
                    )
                else:
                    query_data += '%s.%s %s' % (
                        self._get_collection_ident(self.collections[0]),
                        sorting_entry['field'],
                        sorting_entry['order'],
                    )

                if is_first:
                    is_first = False

        if self.count is not -1:

            if self.start is not -1:
                query_data += ' LIMIT %s, %s' % (self.start, self.count)
            else:
                query_data += ' LIMIT %s' % self.count

        query_data += ' RETURN %s' % collection + '_123'

        post_data = {
            'query': query_data
        }

        api = Client.instance().api

        result = []

        try:
            post_result = api.cursor.post(data=post_data)

            result_dict_list = post_result['result']

            # Create documents
            for result_dict in result_dict_list:
                doc = create_document_from_result_dict(result_dict, api)
                result.append(doc)


        except Exception as err:
            print(err.message)

        return result


    def _get_collection_ident(self, collection_name):
        return collection_name + '_123'


class Traveser(object):
    """
    """

    @classmethod
    def follow(cls, start_vertex, edge_collection, direction):
        """
        """

        related_docs = []

        request_data = {
            'startVertex': start_vertex,
            'edgeCollection': edge_collection,
            'direction': direction,
        }

        api = Client.instance().api
        result_dict = api.traversal.post(data=request_data)
        results = result_dict['result']['visited']

        vertices = results['vertices']
        vertices.remove(vertices[0])

        for vertice in vertices:
            collection_name = vertice['_id'].split('/')[0]

            doc = Document(
                id=vertice['_id'],
                key=vertice['_key'],
                collection=collection_name,
                api=api,
            )

            del vertice['_id']
            del vertice['_key']
            del vertice['_rev']

            doc.data = vertice

            related_docs.append(doc)

        return related_docs