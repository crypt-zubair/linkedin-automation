import unittest
from app.checker import check_post
from app.selector import load_facts

class CoreTests(unittest.TestCase):
    def test_fact_database(self):
        facts = load_facts()
        ids = [int(x['id']) for x in facts]
        self.assertEqual(len(facts), 30)
        self.assertEqual(len(ids), len(set(ids)))

    def test_checker(self):
        fact = {'id': 1, 'category': 'Test', 'fact': 'A computer mouse prototype had a wooden casing.', 'source': 'Test'}
        post = 'A computer mouse prototype had a wooden casing. It is a small reminder that familiar hardware often starts with very different designs. #Technology #ComputerHistory'
        score, _ = check_post(post, fact)
        self.assertGreaterEqual(score, 7.5)

if __name__ == '__main__':
    unittest.main()
