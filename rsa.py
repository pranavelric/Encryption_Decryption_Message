import random
import hashlib

max_PrimLength = 500

'''
calculates the modular inverse from e and phi
'''


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


'''
calculates the gcd of two ints
'''


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
checks if a number is a prime
'''


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


'''
Generate prime numbers
'''


def generateRandomPrim():
    while(1):
        ranPrime = random.randint(0, max_PrimLength)
        if is_prime(ranPrime):
            return ranPrime


'''
Generate key pairs for public and private key
'''


def generate_keyPairs():
    p = generateRandomPrim()
    q = generateRandomPrim()

    n = p*q
    # print("n ", n)
    '''phi(n) = phi(p)*phi(q)'''
    phi = (p-1) * (q-1)
    # print("phi ", phi)

    '''choose e coprime to n and 1 > e > phi'''
    e = random.randint(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)

    # print("e=", e, " ", "phi=", phi)
    '''d[1] = modular inverse of e and phi'''
    d = egcd(e, phi)[1]

    '''make sure d is positive'''
    d = d % phi
    if(d < 0):
        d += phi

    return ((e, n), (d, n))


def rsa_encrypt(e, n, ct):
    final_ans = 1
    for i in range(1, e+1):
        final_ans = (final_ans * ct) % n
    return final_ans


def rsa_decrypt(d, n, ct):
    final_ans = 1
    for i in range(1, d+1):
        final_ans = (final_ans * ct) % n
    return final_ans


'''
hashing function
'''


def hashing(text):
    return hashlib.md5(text.encode())
