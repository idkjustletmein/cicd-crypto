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


class TestCiphersAPIView:
    """Tests for the ciphers API endpoint."""
    
    def test_get_ciphers(self, client):
        response = client.get('/api/ciphers/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 18
        assert 'caesar' in data
