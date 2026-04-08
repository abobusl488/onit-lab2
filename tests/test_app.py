import unittest

class TestApp(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(1, 1)
    
    def test_import(self):
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///:memory:')
        self.assertIsNotNone(engine)

if __name__ == '__main__':
    unittest.main()
