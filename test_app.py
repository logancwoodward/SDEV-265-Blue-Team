import unittest

from app import app  # Import your Flask app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'  # Use a test secret key
        self.client = app.test_client()

    def test_index_page(self):
        """Test if the index page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login_fail(self):
        """Test failed admin login."""
        response = self.client.post('/admin', data={'username': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)

    def test_admin_dashboard_redirect(self):
        """Test access to admin dashboard without login."""
        response = self.client.get('/admin_dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_get_response(self):
        """Test chatbot response retrieval."""
        response = self.client.post('/get_response', json={'message': 'hello'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json)

if __name__ == '__main__':
    unittest.main()
