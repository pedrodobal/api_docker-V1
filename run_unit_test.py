import unittest
from account_controller_test import AccountControllerTestCase
from transaction_controller_test import TransactionControllerTestCase

if __name__ == '__main__':
    account_tests = unittest.TestLoader().loadTestsFromTestCase(AccountControllerTestCase)
    transaction_tests = unittest.TestLoader().loadTestsFromTestCase(TransactionControllerTestCase)
    
    all_tests = unittest.TestSuite([transaction_tests, account_tests])

    unittest.TextTestRunner(verbosity=2).run(all_tests)
