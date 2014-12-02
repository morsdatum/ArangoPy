import timeit
from arangodb.api import Client, Database, Collection


##################################
# These tests
##################################

# Init client
from arangodb.query.advanced import Query
from arangodb.query.simple import SimpleQuery

client = Client('arango.nix.bra')

# Create database in which all collections are created
database_name = 'arangopy_speed_test_database'
try:
    Database.create(database_name)
except:
    client.set_database(database_name)


timer = timeit.default_timer

def timer_decorator(message):
    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            start = timer()
            func(*args, **kwargs)
            elapsed = timer() - start
            print(message % elapsed)

        return wrapper

    return outer_wrapper


document_number = 10**5 # 10 thousand

def timer_decorator2(message):
    def outer_wrapper2(func):
        def wrapper2(*args, **kwargs):
	    global document_number
            start = timer()
            func(*args, **kwargs)
            elapsed = timer() - start
            print(message % (document_number,elapsed))

        return wrapper2

    return outer_wrapper2

@timer_decorator('Adding documents to the collection took %s seconds')
def create_big_number_of_documents(big_collection):
    """
    """

    for i in range(1, document_number):
        doc = big_collection.create_document()
        doc.index = i
        doc.save()

@timer_decorator2('Retrieving %s documents normally from the collection took %s seconds')
def retrieve_normally_documents(big_collection):
    """
    """

    big_collection.documents()

@timer_decorator2('Retrieving %s documents via simple query from the collection took %s seconds')
def retrieve_simply_documents(big_collection):
    """
    """

    SimpleQuery.all(collection=big_collection)

@timer_decorator2('Retrieving %s documents via aql from the collection took %s seconds')
def retrieve_aql_documents(big_collection):
    """
    """

    all_aql_query = Query()
    all_aql_query.append_collection(collection_name=big_collection.name)
    all_aql_query.execute()

# Everything needs to be in one try-catch so we can clean up afterwards
try:

    big_collection_name = 'big_collection'
    big_collection = Collection.create(big_collection_name)

    print('All tests are using either %s documents, edges or models' % document_number)

    # Create first all documents
    create_big_number_of_documents(big_collection)

    # Get all documents normally
    retrieve_normally_documents(big_collection)

    # Get documents with simple query
    retrieve_simply_documents(big_collection)

    # Get documents with aql
    retrieve_aql_documents(big_collection)

    # Delete all documents
    Collection.remove(big_collection_name)

except Exception as err:
    print(err)

# Destroy at the end the database
Database.remove(database_name)
