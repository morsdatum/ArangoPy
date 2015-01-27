from arangodb.tests.base import ExtendedTestCase

from arangodb.api import Database, Collection
from arangodb.query.simple import SimpleQuery


class IntegerDocumentTestCase(ExtendedTestCase):
    def setUp(self):
	self.database_name = 'testcase_int_abc'
	self.collection1_name = 'int32_collection_abc'
	self.collection2_name = 'int64_collection_xyz'
	self.coll3_name = 'dec10_coll_123'
	self.coll4_name = 'dec20_col2_456'
	self.db = Database.create(name=self.database_name)
	self.col1 = self.db.create_collection(self.collection1_name)
	self.col2 = self.db.create_collection(self.collection2_name)
	self.col3 = self.db.create_collection(self.coll3_name)
	self.col4 = self.db.create_collection(self.coll4_name)

    def tearDown(self):
	Collection.remove(name=self.collection1_name)
	Collection.remove(name=self.collection2_name)
	Collection.remove(name=self.coll3_name)
	Collection.remove(name=self.coll4_name)
	Database.remove(name=self.database_name)

    def test_int32_doc_save(self):
        for x in xrange(300):
            doc = self.col1.create_document()
            doc.int32 = 2**32
	    doc.int32_1 = 2**32 - 1
	    doc.int31 = 2**31
	    doc.int31_1 = 2**31 - 1
	    doc.save()

	docs = SimpleQuery.all(self.col1)

	self.assertEqual(len(docs),300)

	for x in xrange(len(docs)):
            self.assertEqual(docs[x].int32,2**32)
	    self.assertEqual(docs[x].int32_1,2**32 - 1)
	    self.assertEqual(docs[x].int31,2**31)
	    self.assertEqual(docs[x].int31_1,2**31 - 1)

    def test_dec10_save(self):
	for i in xrange(100):
            doc = self.col3.create_document()
	    doc.dec10 = 10**10;
	    doc.dec10_1 = 10**10 - 1
	    doc.dec9 = 10**9
	    doc.dec9_1 = 10**9 - 1
	    doc.save()

	docs = SimpleQuery.all(self.col3)

	self.assertEqual(len(docs),100)

	for j in xrange(len(docs)):
	    self.assertEqual(docs[j].dec10,10**10)
	    self.assertEqual(docs[j].dec10_1,10**10 - 1)
	    self.assertEqual(docs[j].dec9,10**9)
	    self.assertEqual(docs[j].dec9_1,10**9 - 1)

    def test_dec19_save(self):
	for i in xrange(100):
            doc = self.col4.create_document()
	    doc.dec18 = 10**15;
	    doc.dec18_1 = 10**15 - 1
	    doc.dec17 = 10**14
	    doc.dec17_1 = 10**14 - 1
	    doc.save()

	docs = SimpleQuery.all(self.col4)

	self.assertEqual(len(docs),100)

	for j in xrange(len(docs)):
	    self.assertEqual(docs[j].dec18,10**15)
	    self.assertEqual(docs[j].dec18_1,10**15 - 1)
	    self.assertEqual(docs[j].dec17,10**14)
	    self.assertEqual(docs[j].dec17_1,10**14 - 1)
	     

    def test_int64_doc_save(self):
	for y in xrange(300):
	    doc = self.col2.create_document()
	    doc.int62 = 2**52
	    doc.int62_1 = 2**52 - 1
	    doc.int63 = 2**53
	    doc.int63_1 = 2**53 - 1
	    doc.save()

	docs = SimpleQuery.all(self.col2)

	self.assertEqual(len(docs),300)

	for y in xrange(len(docs)):
	    self.assertEqual(docs[y].int62,2**52)
	    self.assertEqual(docs[y].int62_1,2**52 - 1)
	    self.assertEqual(docs[y].int63,2**53)
	    self.assertEqual(docs[y].int63_1,2**53 - 1)
