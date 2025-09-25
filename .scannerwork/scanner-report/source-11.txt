import os
import json
import random

KEY_DIR = "rsa_app/keys"
KEY_FILE = os.path.join(KEY_DIR, "rsa_keys.json")

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Inverse modulaire non existant')
    else:
        return x % m

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime_candidate(start=100, end=300):
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p

def regenerate_keys():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

    p = generate_prime_candidate()
    q = generate_prime_candidate()
    while q == p:
        q = generate_prime_candidate()

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    try:
        d = modinv(e, phi)
    except Exception:
        return regenerate_keys()  # relance si modinv échoue

    keys = {
        "n": n,
        "e": e,
        "d": d
    }
    with open(KEY_FILE, "w") as f:
        json.dump(keys, f)
    return keys

def load_keys():
    with open(KEY_FILE, "r") as f:
        return json.load(f)

def encrypt(message_int, e, n):
    return pow(message_int, e, n)

def decrypt(cipher_int, d, n):
    return pow(cipher_int, d, n)
