"""Views for CryptoLab application."""

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .ciphers import get_cipher, get_all_ciphers


@require_http_methods(["GET"])
def index(request):
    """Render the main page."""
    ciphers = get_all_ciphers()
    return render(request, 'index.html', {'ciphers': ciphers})


@require_http_methods(["GET"])
def learn(request):
    """Render the learn page."""
    ciphers = get_all_ciphers()
    return render(request, 'learn.html', {'ciphers': ciphers})


def compare(request):
    """Render the compare page."""
    ciphers = get_all_ciphers()
    return render(request, 'compare.html', {'ciphers': ciphers})


@require_http_methods(["GET"])
def about(request):
    """Render the about page."""
    return render(request, 'about.html')


@require_http_methods(["GET"])
def security(request):
    """Render the security tools page."""
    return render(request, 'security.html')



@require_http_methods(["POST"])
def encrypt(request):
    """Encrypt plaintext using the specified cipher."""
    try:
        data = json.loads(request.body)
        cipher_name = data.get('cipher')
        plaintext = data.get('plaintext', '')
        key = data.get('key', '')
        
        if not cipher_name:
            return JsonResponse({'error': 'Cipher not specified'}, status=400)
        
        cipher_class = get_cipher(cipher_name)
        if not cipher_class:
            return JsonResponse({'error': f'Unknown cipher: {cipher_name}'}, status=400)
        
        # Validate key
        is_valid, error_msg = cipher_class.validate_key(key)
        if not is_valid:
            return JsonResponse({'error': error_msg}, status=400)
        
        cipher = cipher_class()
        result = cipher.encrypt(plaintext, key)
        
        return JsonResponse({
            'result': result,
            'cipher_info': {
                'name': cipher_class.name,
                'description': cipher_class.description,
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Encryption failed: {str(e)}'}, status=500)


@require_http_methods(["POST"])
def decrypt(request):
    """Decrypt ciphertext using the specified cipher."""
    try:
        data = json.loads(request.body)
        cipher_name = data.get('cipher')
        ciphertext = data.get('ciphertext', '')
        key = data.get('key', '')
        
        if not cipher_name:
            return JsonResponse({'error': 'Cipher not specified'}, status=400)
        
        cipher_class = get_cipher(cipher_name)
        if not cipher_class:
            return JsonResponse({'error': f'Unknown cipher: {cipher_name}'}, status=400)
        
        # Validate key
        is_valid, error_msg = cipher_class.validate_key(key)
        if not is_valid:
            return JsonResponse({'error': error_msg}, status=400)
        
        cipher = cipher_class()
        result = cipher.decrypt(ciphertext, key)
        
        return JsonResponse({
            'result': result,
            'cipher_info': {
                'name': cipher_class.name,
                'description': cipher_class.description,
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Decryption failed: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def get_ciphers(request):
    """Return information about all available ciphers."""
    return JsonResponse(get_all_ciphers())

# ...
# INTENTIONAL DUPLICATION TO TRIGGER SONARCLOUD FAILURE
# ...
@require_http_methods(["POST"])
def encrypt_duplicate_for_sonar_test(request):
    """Encrypt plaintext using the specified cipher."""
    try:
        data = json.loads(request.body)
        cipher_name = data.get('cipher')
        plaintext = data.get('plaintext', '')
        key = data.get('key', '')
        
        if not cipher_name:
            return JsonResponse({'error': 'Cipher not specified'}, status=400)
        
        cipher_class = get_cipher(cipher_name)
        if not cipher_class:
            return JsonResponse({'error': f'Unknown cipher: {cipher_name}'}, status=400)
        
        # Validate key
        is_valid, error_msg = cipher_class.validate_key(key)
        if not is_valid:
            return JsonResponse({'error': error_msg}, status=400)
        
        cipher = cipher_class()
        result = cipher.encrypt(plaintext, key)
        
        return JsonResponse({
            'result': result,
            'cipher_info': {
                'name': cipher_class.name,
                'description': cipher_class.description,
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Encryption failed: {str(e)}'}, status=500)

