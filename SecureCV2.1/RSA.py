
import random
# from fractions import Fraction
from math import gcd

def extendedEuclidean(num1, num2):
    if num2 == 0:
        return (num1, 1, 0)

    d, temp_x, temp_y = extendedEuclidean(num2, num1 % num2)
    
    x, y = temp_y, temp_x - int(num1 / num2) * temp_y

    return (d, x, y)

def rabinMillerTest(p, iteration):
    if p < 2:
        return False
    if p != 2 and p % 2 == 0:
        return False
    s = p-1
    while s % 2 == 0:
        s //= 2
    for i in range(iteration):
        a = random.randint(1, p-1)
        temp = s
        mod = pow(a, temp, p)  # Computes (a^temp)%p
        while temp != p-1 and mod != 1 and mod != p-1:
            mod = pow(mod, mod, p)
            temp *= 2

        if mod != p-1 and temp % 2 == 0:
            return False

    return True


def multiplicativeInverse(a, b, n):
    d, x, y = extendedEuclidean(a, n)
    if b % d == 0:
        temp_x = (x * (b/d)) % n
        result = []
        for i in range(d):
            result.append((temp_x + i*(n/d)) % n)
        return result
    return []


def generateRandomPrime(bits):
    num = random.getrandbits(bits - 1)
    if num % 2 == 0:
        num -= 1
    num += (1 << (bits - 1))
    while(not rabinMillerTest(num, 40)):
        num += 2

    return num


def generate(bits=512):
    p = generateRandomPrime(bits//2)
    q = p
    while q == p:
        q = generateRandomPrime(bits//2)
    n = p*q
    phi = (p-1) * (q-1)
    e = random.randint(1, 50000)
    e = 2*e + 1
    while not (gcd(phi, e) == 1):
        e = random.randint(1, 50000)
        e = 2*e + 1
    
    d = multiplicativeInverse(e, 1, phi)[0]
    return {
        "public": (e, n),
        "private": (int(d), n)
    }


def encrypt(keys, text):
    """
    :param
    """
    key, n = keys
    result = [pow(ord(c), key, n) for c in text]
    return result


def decrypt(keys, text):
    # NOTE: The mathematical function implemented by both the encrypt
    # and decrypt functions are exactly the same. We can call encrypt
    # again to decrypt our ciphertext. But the problem is encrypt converts
    # text from characters to extremely large numbers which can not be
    # encoded in characters. So calling chr(on_extremely_large_number)
    # will throw some kind of error
    key, n = keys
    result = [chr(pow(int(c), int(key), int(n) )) for c in text]
    return ''.join(result)

