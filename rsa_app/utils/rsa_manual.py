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

def generate_keys():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = modinv(e, phi)
    return {'n': n, 'e': e, 'd': d}

def encrypt(message, e, n):
    return pow(message, e, n)

def decrypt(cipher, d, n):
    return pow(cipher, d, n)
