"""Views for CryptoLab application."""

import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from .ciphers import get_cipher, get_all_ciphers
from .forms import RegisterForm, KeyFileUploadForm
from .models import CryptoHistory, UploadedKeyFile

INVALID_JSON_ERROR = 'Invalid JSON'


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


@require_http_methods(["GET"])
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


# ─── Authentication Views ─────────────────────────────────────────

@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to CryptoLab, {user.username}!')
            return redirect('index')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            if not url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                next_url = '/'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('index')


# ─── History Views ─────────────────────────────────────────────────

@login_required
@require_http_methods(["GET"])
def history_view(request):
    """Render the history page for authenticated users."""
    history = CryptoHistory.objects.filter(user=request.user)[:50]
    return render(request, 'history.html', {'history': history})


@login_required
@require_http_methods(["GET"])
def api_history(request):
    """Return user's encryption history as JSON."""
    history = CryptoHistory.objects.filter(user=request.user)[:50]
    data = [
        {
            'id': entry.id,
            'cipher': entry.cipher,
            'operation': entry.operation,
            'input_text': entry.input_text,
            'output_text': entry.output_text,
            'key_used': entry.key_used,
            'timestamp': entry.timestamp.isoformat(),
        }
        for entry in history
    ]
    return JsonResponse({'history': data})


@login_required
@require_http_methods(["POST"])
def api_delete_history(request):
    """Delete a history entry."""
    try:
        data = json.loads(request.body)
        entry_id = data.get('id')
        
        if not entry_id:
            return JsonResponse({'error': 'Missing entry ID'}, status=400)
        
        entry = CryptoHistory.objects.filter(id=entry_id, user=request.user).first()
        if not entry:
            return JsonResponse({'error': 'Entry not found'}, status=404)
        
        entry.delete()
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'error': INVALID_JSON_ERROR}, status=400)


# ─── File Upload Views ─────────────────────────────────────────────

@login_required
@require_http_methods(["GET", "POST"])
def upload_key_view(request):
    """Handle key file uploads."""
    if request.method == 'POST':
        form = KeyFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['key_file']
            key_file = UploadedKeyFile(
                user=request.user,
                file=uploaded_file,
                original_filename=uploaded_file.name,
                cipher_type=form.cleaned_data.get('cipher_type', ''),
            )
            key_file.save()
            
            # Read the key content
            key_file.file.seek(0)
            key_content = key_file.file.read().decode('utf-8', errors='replace').strip()
            
            return JsonResponse({
                'success': True,
                'key_content': key_content,
                'filename': uploaded_file.name,
            })
        else:
            return JsonResponse({'error': 'Invalid file'}, status=400)
    
    # GET: show upload form and list of uploaded files
    files = UploadedKeyFile.objects.filter(user=request.user)[:20]
    form = KeyFileUploadForm()
    return render(request, 'upload_key.html', {'form': form, 'files': files})


@login_required
@require_http_methods(["POST"])
def api_upload_key(request):
    """API endpoint for key file upload."""
    if not request.FILES.get('key_file'):
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    uploaded_file = request.FILES['key_file']
    cipher_type = request.POST.get('cipher_type', '')
    
    key_file = UploadedKeyFile(
        user=request.user,
        file=uploaded_file,
        original_filename=uploaded_file.name,
        cipher_type=cipher_type,
    )
    key_file.save()
    
    key_file.file.seek(0)
    key_content = key_file.file.read().decode('utf-8', errors='replace').strip()
    
    return JsonResponse({
        'success': True,
        'key_content': key_content,
        'filename': uploaded_file.name,
        'id': key_file.id,
    })


# ─── Encrypt / Decrypt (with history saving) ──────────────────────

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
        
        # Save to history if user is authenticated
        if request.user.is_authenticated:
            CryptoHistory.objects.create(
                user=request.user,
                cipher=cipher_name,
                operation='encrypt',
                input_text=plaintext,
                output_text=result,
                key_used=key,
            )
        
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
    except Exception:
        return JsonResponse({'error': 'Encryption failed due to an internal server error.'}, status=500)


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
        
        # Save to history if user is authenticated
        if request.user.is_authenticated:
            CryptoHistory.objects.create(
                user=request.user,
                cipher=cipher_name,
                operation='decrypt',
                input_text=ciphertext,
                output_text=result,
                key_used=key,
            )
        
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
    except Exception:
        return JsonResponse({'error': 'Decryption failed due to an internal server error.'}, status=500)


@require_http_methods(["GET"])
def get_ciphers(request):
    """Return information about all available ciphers."""
    return JsonResponse(get_all_ciphers())
