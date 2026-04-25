"""Tests for Django views."""

import json
import pytest
from django.test import Client


@pytest.fixture
def client():
    """Create a test client."""
    return Client()


class TestIndexView:
    """Tests for the index view."""
    
    def test_index_returns_200(self, client):
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_contains_ciphers(self, client):
        response = client.get('/')
        content = response.content.decode()
        assert 'Caesar' in content
        assert 'Vigenère' in content


class TestEncryptView:
    """Tests for the encrypt API endpoint."""
    
    def test_encrypt_caesar(self, client):
        response = client.post(
            '/encrypt/',
            data=json.dumps({
                'cipher': 'caesar',
                'plaintext': 'HELLO',
                'key': '3'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'KHOOR'
    
    def test_encrypt_missing_cipher(self, client):
        response = client.post(
            '/encrypt/',
            data=json.dumps({
                'plaintext': 'HELLO',
                'key': '3'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_encrypt_invalid_cipher(self, client):
        response = client.post(
            '/encrypt/',
            data=json.dumps({
                'cipher': 'nonexistent',
                'plaintext': 'HELLO',
                'key': '3'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_encrypt_invalid_key(self, client):
        response = client.post(
            '/encrypt/',
            data=json.dumps({
                'cipher': 'caesar',
                'plaintext': 'HELLO',
                'key': 'abc'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_encrypt_internal_server_error(self, client):
        from unittest.mock import patch
        with patch('cryptolab.ciphers.caesar.CaesarCipher.encrypt', side_effect=Exception("Simulated failure")):
            response = client.post(
                '/encrypt/',
                data=json.dumps({
                    'cipher': 'caesar',
                    'plaintext': 'HELLO',
                    'key': '3'
                }),
                content_type='application/json'
            )
            assert response.status_code == 500
            assert response.json()['error'] == 'Encryption failed due to an internal server error.'


class TestDecryptView:
    """Tests for the decrypt API endpoint."""
    
    def test_decrypt_caesar(self, client):
        response = client.post(
            '/decrypt/',
            data=json.dumps({
                'cipher': 'caesar',
                'ciphertext': 'KHOOR',
                'key': '3'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'HELLO'
    
    def test_decrypt_vigenere(self, client):
        response = client.post(
            '/decrypt/',
            data=json.dumps({
                'cipher': 'vigenere',
                'ciphertext': 'RIJVS',
                'key': 'KEY'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'HELLO'

    def test_decrypt_internal_server_error(self, client):
        from unittest.mock import patch
        with patch('cryptolab.ciphers.caesar.CaesarCipher.decrypt', side_effect=Exception("Simulated failure")):
            response = client.post(
                '/decrypt/',
                data=json.dumps({
                    'cipher': 'caesar',
                    'ciphertext': 'KHOOR',
                    'key': '3'
                }),
                content_type='application/json'
            )
            assert response.status_code == 500
            assert response.json()['error'] == 'Decryption failed due to an internal server error.'


class TestCiphersAPIView:
    """Tests for the ciphers API endpoint."""
    
    def test_get_ciphers(self, client):
        response = client.get('/api/ciphers/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 15
        assert 'caesar' in data

    def test_learn_view(self, client):
        """Test the learn view returns 200."""
        response = client.get('/learn/')
        assert response.status_code == 200
        assert b"Learn Cryptography" in response.content

    def test_about_view(self, client):
        """Test the about view returns 200."""
        response = client.get('/about/')
        assert response.status_code == 200
        assert b"About CryptoLab" in response.content

    def test_security_view(self, client):
        """Test the security view returns 200."""
        response = client.get('/security/')
        assert response.status_code == 200
        assert b"Password Security Check" in response.content


from django.contrib.auth.models import User
from cryptolab.models import CryptoHistory, UploadedKeyFile
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def auth_client():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword123', email='test@example.com')
    client.login(username='testuser', password='testpassword123')
    return client, user


class TestAuthViews:
    """Tests for authentication views."""
    
    @pytest.mark.django_db
    def test_register_view_get(self, client):
        response = client.get('/register/')
        assert response.status_code == 200
        assert b"Create Account" in response.content

    @pytest.mark.django_db
    def test_login_view_get(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assert b"Sign In" in response.content

    @pytest.mark.django_db
    def test_logout_redirect(self, client):
        response = client.get('/logout/')
        assert response.status_code == 302
        assert response.url == '/'

    @pytest.mark.django_db
    def test_login_view_redirects_safe_next_url(self, auth_client):
        client, user = auth_client
        client.logout()  # ensure logged out first
        response = client.post('/login/?next=/learn/', {'username': 'testuser', 'password': 'testpassword123'})
        assert response.status_code == 302
        assert response.url == '/learn/'

    @pytest.mark.django_db
    def test_login_view_ignores_unsafe_next_url(self, auth_client):
        client, user = auth_client
        client.logout()
        # Should override to '/'
        response = client.post('/login/?next=https://evil.com/phishing', {'username': 'testuser', 'password': 'testpassword123'})
        assert response.status_code == 302
        assert response.url == '/'


class TestHistory:
    """Tests for history functionality."""

    @pytest.mark.django_db
    def test_history_view_authenticated(self, auth_client):
        client, user = auth_client
        CryptoHistory.objects.create(
            user=user, cipher='caesar', operation='encrypt',
            input_text='HELLO', output_text='KHOOR', key_used='3'
        )
        response = client.get('/history/')
        assert response.status_code == 200
        assert b"KHOOR" in response.content

    @pytest.mark.django_db
    def test_history_view_unauthenticated(self, client):
        response = client.get('/history/')
        assert response.status_code == 302
        assert '/login/?next=/history/' in response.url

    @pytest.mark.django_db
    def test_api_history(self, auth_client):
        client, user = auth_client
        CryptoHistory.objects.create(
            user=user, cipher='caesar', operation='encrypt',
            input_text='HELLO', output_text='KHOOR', key_used='3'
        )
        response = client.get('/api/history/')
        assert response.status_code == 200
        data = response.json()
        assert len(data['history']) == 1
        assert data['history'][0]['cipher'] == 'caesar'

    @pytest.mark.django_db
    def test_encrypt_saves_history(self, auth_client):
        client, user = auth_client
        response = client.post(
            '/encrypt/',
            data=json.dumps({'cipher': 'caesar', 'plaintext': 'TEST', 'key': '1'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert CryptoHistory.objects.filter(user=user).count() == 1

    @pytest.mark.django_db
    def test_api_delete_history_missing_id(self, auth_client):
        client, _ = auth_client
        response = client.post('/api/history/delete/', data=json.dumps({}), content_type='application/json')
        assert response.status_code == 400
        assert response.json()['error'] == 'Missing entry ID'

    @pytest.mark.django_db
    def test_api_delete_history_not_found(self, auth_client):
        client, user = auth_client
        response = client.post('/api/history/delete/', data=json.dumps({'id': 9999}), content_type='application/json')
        assert response.status_code == 404
        assert response.json()['error'] == 'Entry not found'

    @pytest.mark.django_db
    def test_api_delete_history_invalid_json(self, auth_client):
        client, user = auth_client
        response = client.post(
            '/api/history/delete/',
            data="not-valid-json",
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'Invalid JSON'

    @pytest.mark.django_db
    def test_encrypt_invalid_cipher(self, client):
        response = client.post(
            '/encrypt/',
            data=json.dumps({'cipher': 'unknown_cipher', 'plaintext': 'TEST', 'key': '1'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'Unknown cipher' in response.json()['error']

    @pytest.mark.django_db
    def test_encrypt_missing_cipher(self, client):
        response = client.post('/encrypt/', data=json.dumps({'plaintext': 'TEST'}), content_type='application/json')
        assert response.status_code == 400
        assert response.json()['error'] == 'Cipher not specified'

    @pytest.mark.django_db
    def test_encrypt_invalid_key(self, client):
        response = client.post('/encrypt/', data=json.dumps({'cipher': 'caesar', 'plaintext': 'TEST', 'key': 'not_an_int'}), content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_encrypt_invalid_json(self, client):
        response = client.post(
            '/encrypt/',
            data="invalid-json-{",
            content_type="application/json"
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'Invalid JSON'


class TestFileUpload:
    """Tests for key file upload."""

    @pytest.mark.django_db
    def test_upload_key_view_get(self, auth_client):
        client, _ = auth_client
        response = client.get('/upload-key/')
        assert response.status_code == 200
        assert b"Upload Key File" in response.content

    @pytest.mark.django_db
    def test_api_upload_key(self, auth_client):
        client, user = auth_client
        test_file = SimpleUploadedFile("test_key.txt", b"my_secret_key", content_type="text/plain")
        response = client.post(
            '/api/upload-key/',
            {'key_file': test_file, 'cipher_type': 'AES'}
        )
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['key_content'] == 'my_secret_key'
        assert UploadedKeyFile.objects.filter(user=user).count() == 1

    @pytest.mark.django_db
    def test_api_upload_key_missing_file(self, auth_client):
        client, user = auth_client
        response = client.post('/api/upload-key/', {'cipher_type': 'AES'})
        assert response.status_code == 400
        assert response.json()['error'] == 'No file provided'

    @pytest.mark.django_db
    def test_upload_key_view_invalid_form(self, auth_client):
        client, user = auth_client
        response = client.post('/upload-key/', {'cipher_type': 'AES'})
        assert response.status_code == 400
        assert response.json()['error'] == 'Invalid file'


class TestSettings:
    """Tests for settings configuration."""
    
    def test_production_secret_key_check(self):
        import importlib
        import os
        from cryptolab import settings
        
        orig_debug = os.environ.get('DEBUG')
        orig_key = os.environ.get('DJANGO_SECRET_KEY')
        
        try:
            os.environ['DEBUG'] = 'False'
            os.environ['DJANGO_SECRET_KEY'] = 'django-insecure-dev-key-change-in-production'
            
            with pytest.raises(ValueError, match="DJANGO_SECRET_KEY must be set in production"):
                importlib.reload(settings)
        finally:
            if orig_debug is not None:
                os.environ['DEBUG'] = orig_debug
            else:
                os.environ.pop('DEBUG', None)
                
            if orig_key is not None:
                os.environ['DJANGO_SECRET_KEY'] = orig_key
            else:
                os.environ.pop('DJANGO_SECRET_KEY', None)
                
            importlib.reload(settings)
