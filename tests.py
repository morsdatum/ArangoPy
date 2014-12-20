# Unit Tests
import unittest

# Test suites
from arangodb.tests import *


# Variables

test_suites = []
errors = 0
failures = 0

# Test suites
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DatabaseTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DocumentTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(AqlQueryTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(SimpleQueryTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(SimpleIndexQueryTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(IntegerDocumentTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TraveserTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelManagerTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelManagerForIndexTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CollectionModelForeignKeyFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ListFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DictFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(BooleanFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(CharFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(UuidFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ChoiceFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(NumberFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DateFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(DatetimeFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ForeignkeyFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(ManyToManyFieldTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TransactionTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(IndexTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(UserTestCase) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(EndpointTestCase) )

for test_suite in test_suites:

    # Tests runner
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)

    errors += len(result.errors)
    failures += len(result.failures)

import sys; sys.exit( errors + failures )
