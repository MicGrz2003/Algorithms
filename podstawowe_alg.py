import math
import timeit
import matplotlib.pyplot as plt
import random
from math import gcd


def czynniki_pierwsze(n, k = 2):
    dzielniki = []
    while k <= math.isqrt(n):
        if n % k == 0:
            dzielniki.append(k)
            dzielniki.extend(czynniki_pierwsze(n // k, k))
            return dzielniki
        k += 1

    if n > 1:
        dzielniki.append(n)
    return dzielniki

print(czynniki_pierwsze(12))
print(czynniki_pierwsze(1500))

def sito_Eratostenesa(n):
    pierwsze = [True] * (n + 1)
    pierwsze[0] = pierwsze[1] = False 
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if pierwsze[i]:
            for j in range(i*i, n+1, i):
                pierwsze[j] = False
                
    return [i for i in range(2, n+1) if pierwsze[i]]

print(sito_Eratostenesa(12))
print(sito_Eratostenesa(130))

def RNWD(a, b):
    czynniki_a = czynniki_pierwsze(a)
    czynniki_b = czynniki_pierwsze(b)
    
    i = j = 0
    NWD = 1
    while i < len(czynniki_a) and j < len(czynniki_b):
        if czynniki_a[i] < czynniki_b[j]:
            i += 1
        elif czynniki_a[i] > czynniki_b[j]:
            j += 1
        else:
            NWD *= czynniki_a[i]
            i += 1
            j += 1
    
    return NWD

print("RNWD", RNWD(12, 20))
print("RNWD", RNWD(630, 2430))

def ENWD(a, b) : 
    while b != 0 : 
        a, b = b, a % b
    return a

print("ENWD", ENWD(12, 20))
print("ENWD", ENWD(630, 2430))

def czas(n, m):
    times_RNWD = []
    times_ENWD = []
    for q in range(1, m+1):
        time_RNWD = timeit.timeit(lambda: RNWD(n, q), number=1)
        time_ENWD = timeit.timeit(lambda: ENWD(n, q), number=1)
        times_RNWD.append(time_RNWD)
        times_ENWD.append(time_ENWD)
    
    return times_RNWD, times_ENWD

def wykres(n, m):
    q_values = list(range(1, m+1))
    times_RNWD, times_ENWD = czas(n, m)
    
    plt.plot(q_values, times_RNWD, label='RNWD')
    plt.plot(q_values, times_ENWD, label='ENWD')
    plt.xlabel('q')
    plt.ylabel('Czas (s)')
    plt.title('Czas działania algorytmów RNWD i ENWD')
    plt.legend()
    plt.show()

wykres(12, 20)
wykres(630, 2430)

def potegowanie_modulo_szybkie(a, n, p):
    wynik = 1
    a = a % p
    while n > 0:
        if n % 2 == 1:
            wynik = (wynik * a) % p
        a = (a * a) % p
        n //= 2
    return wynik

def test_Fermata(p, k=10):
    if p == 2:
        return True
    if p < 2 or p % 2 == 0:
        return False
    
    for _ in range(k):
        a = random.randint(2, p - 1)
        if potegowanie_modulo_szybkie(a, p - 1, p) != 1:
            return False
    return True

print("Wynik testu Fermata 14021:", test_Fermata(14021))
print("Wynik testu Fermata 3001:",test_Fermata(3001))

def test_Miller_Rabina(p, k=10):
    if p == 2:
        return True
    if p < 2 or p % 2 == 0:
        return False
    
    def sprawdzenie(a, d, r, p):
        x = potegowanie_modulo_szybkie(a, d, p)
        if x == 1 or x == p - 1:
            return False
        for _ in range(r - 1):
            x = (x * x) % p
            if x == p - 1:
                return False
        return True
    
    d = p - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    for _ in range(k):
        a = random.randint(2, p - 1)
        if sprawdzenie(a, d, r, p):
            return False
    return True

print("Wynik testu Millera Rabina dla 14021:",test_Miller_Rabina(14021))
print("Wynik testu Millera Rabina dla 3001:",test_Miller_Rabina(3001))

def generuj_klucze(p, q):
    """
    Generuje klucze RSA na podstawie liczb pierwszych p i q.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    d = pow(e, -1, phi)
    
    return (e, n), (d, n)

def szyfruj(tekst, klucz_publiczny):
    """
    Szyfruje tekst za pomocą klucza publicznego.
    """
    e, n = klucz_publiczny
    szyfrogram = [pow(ord(znak), e, n) for znak in tekst]
    return szyfrogram

def deszyfruj(szyfrogram, klucz_prywatny):
    """
    Deszyfruje szyfrogram za pomocą klucza prywatnego.
    """
    d, n = klucz_prywatny
    odszyfrowany_tekst = ''.join([chr(pow(znak, d, n)) for znak in szyfrogram])
    return odszyfrowany_tekst

p1, q1 = 2003, 3001
n1 = p1 * q1
phi1 = (p1 - 1) * (q1 - 1)
klucz_publiczny1, klucz_prywatny1 = generuj_klucze(p1, q1)
print("Przykład 1:")
print("p*q =", n1)
print("𝜑(p*q) =", phi1)
print("Klucz publiczny (e, n):", klucz_publiczny1)
print("Klucz prywatny (d, n):", klucz_prywatny1)

tekst1 = "28981"
szyfrogram1 = szyfruj(tekst1, klucz_publiczny1)
odszyfrowany_tekst1 = deszyfruj(szyfrogram1, klucz_prywatny1)
print("\nSzyfrogram dla tekstu 1:", szyfrogram1)
print("Odszyfrowany tekst 1:", odszyfrowany_tekst1)

tekst2 = "2213"
szyfrogram1 = szyfruj(tekst2, klucz_publiczny1)
odszyfrowany_tekst2 = deszyfruj(szyfrogram1, klucz_prywatny1)
print("\nSzyfrogram dla tekstu 1:", szyfrogram1)
print("Odszyfrowany tekst 1:", odszyfrowany_tekst2)

tekst3 = "ciekawy tekst"
szyfrogram1 = szyfruj(tekst3, klucz_publiczny1)
odszyfrowany_tekst3 = deszyfruj(szyfrogram1, klucz_prywatny1)
print("\nSzyfrogram dla tekstu 1:", szyfrogram1)
print("Odszyfrowany tekst 1:", odszyfrowany_tekst3)

p2, q2 = 191, 199
n2 = p2 * q2
phi2 = (p2 - 1) * (q2 - 1)
klucz_publiczny2, klucz_prywatny2 = generuj_klucze(p2, q2)
print("\nPrzykład 2:")
print("p*q =", n2)
print("𝜑(p*q) =", phi2)
print("Klucz publiczny (e, n):", klucz_publiczny2)
print("Klucz prywatny (d, n):", klucz_prywatny2)

tekst1 = "28981"
szyfrogram2 = szyfruj(tekst1, klucz_publiczny2)
odszyfrowany_tekst1 = deszyfruj(szyfrogram2, klucz_prywatny2)
print("\nSzyfrogram dla tekstu 2:", szyfrogram2)
print("Odszyfrowany tekst 2:", odszyfrowany_tekst1)

tekst2 = "2213"
szyfrogram2 = szyfruj(tekst2, klucz_publiczny2)
odszyfrowany_tekst2 = deszyfruj(szyfrogram2, klucz_prywatny2)
print("\nSzyfrogram dla tekstu 2:", szyfrogram2)
print("Odszyfrowany tekst 2:", odszyfrowany_tekst2)

tekst3 = "ciekawy tekst"
szyfrogram2 = szyfruj(tekst3, klucz_publiczny2)
odszyfrowany_tekst3 = deszyfruj(szyfrogram2, klucz_prywatny2)
print("\nSzyfrogram dla tekstu 2:", szyfrogram2)
print("Odszyfrowany tekst 2:", odszyfrowany_tekst3)