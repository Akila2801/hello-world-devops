import unittest
from app import app

class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_hello_returns_200(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_hello_contains_text(self):
        response = self.app.get('/')
        self.assertIn(b'Hello World', response.data)

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
