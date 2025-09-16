from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .rsa_utils import load_keys, encrypt, decrypt, regenerate_keys


def index(request):
    return render(request, 'index.html')

def keys_page(request):
    keys = load_keys()
    return render(request, 'keys.html', {'keys': keys})
@csrf_exempt
def generate_keys_api(request):
    if request.method == 'POST':
        keys = regenerate_keys()
        return JsonResponse({'status': 'success', 'keys': keys})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

def crypt_page(request):
    keys = load_keys()
    return render(request, 'crypt.html', {'keys': keys})

def decrypt_page(request):
    keys = load_keys()
    return render(request, 'decrypt.html', {'keys': keys})

def public_key_api(request):
    keys = load_keys()
    return JsonResponse({'n': keys['n'], 'e': keys['e']})

def decrypt_api(request):
    if request.method == 'POST':
        cipher = int(request.POST.get('cipher'))
        keys = load_keys()
        decrypted = decrypt(cipher, keys['d'], keys['n'])
        try:
            decrypted_bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, 'big')
            message = decrypted_bytes.decode()
        except:
            message = str(decrypted)
        return JsonResponse({'message': message})

def public_key_api(request):
    keys = load_keys()
    return JsonResponse({'n': keys['n'], 'e': keys['e']})

def private_key_api(request):
    keys = load_keys()
    return JsonResponse({'d': str(keys['d']), 'n': str(keys['n'])})

def decrypt_page(request):
    return render(request, 'decrypt.html')
