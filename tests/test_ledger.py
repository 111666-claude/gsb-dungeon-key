import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dkeys.ledger import Ledger  # noqa: E402


class LedgerTest(unittest.TestCase):
    def test_first_issue_succeeds(self):
        self.assertTrue(Ledger(1).issue("r1", "p", 1, 0))

    def test_limit_is_enforced(self):
        ledger = Ledger(1)
        ledger.issue("r1", "p", 1, 0)
        self.assertFalse(ledger.issue("r2", "p", 1, 10))

    def test_work_starts_at_zero(self):
        self.assertEqual(Ledger(1).work_count(), 0)


if __name__ == "__main__":
    unittest.main()
