import unittest

from app import app


class AppTestCase(unittest.TestCase):
	def setUp(self):
		self.client = app.test_client()

	def test_index(self):
		rv = self.client.get('/')
		self.assertEqual(rv.status_code, 200)
		self.assertIn(b'Hello World', rv.data)

	def test_health(self):
		rv = self.client.get('/health')
		self.assertEqual(rv.status_code, 200)
		data = rv.get_json()
		self.assertIsNotNone(data)
		self.assertEqual(data.get('status'), 'ok')


if __name__ == '__main__':
	unittest.main()
