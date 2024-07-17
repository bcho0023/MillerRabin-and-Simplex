"""
Name: Brian Choo Way Yip
Student_Id: 31056334
"""

import random
import sys
import time


def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:

        # Check if the least significant bit is 1
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus

        exponent >>= 1

    return result


def MillerRabinRandomizedPrimality(n, k):
    # if n % 2 == 0:
    #     return False

    s = 0
    t = n - 1
    while modular_exponentiation(t, 1, 2) == 0:
        s += 1
        t //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)

        if modular_exponentiation(a, n - 1, n) != 1:
            return False

        for i in range(1, s + 1):
            previous = modular_exponentiation(a, 2 ** (i - 1) * t, n)
            current = modular_exponentiation(previous, 2, n)

            if current == 1 and previous == 1 and previous == n - 1:
                return False

    return True


def generate_primes(d, k):
    x = d

    while True:
        p = 2 ** x - 1
        if MillerRabinRandomizedPrimality(p, k):
            x += 1
            break
        x += 1

    while True:
        q = 2 ** x - 1
        if MillerRabinRandomizedPrimality(q, k):
            break
        x += 1

    return p, q


def euclidean_gcd(a, b):
    while b != 0:
        a, b = b, modular_exponentiation(a, 1, b)
    return a


def generate_lambda(p, q):
    lam = ((p - 1) * (q - 1)) // euclidean_gcd((p - 1), (q - 1))
    e = random.randint(3, lam - 1)
    while euclidean_gcd(e, lam) != 1:
        e = random.randint(3, lam - 1)
    return e


if __name__ == "__main__":
    _, d = sys.argv
    k = 40
    primes = generate_primes(int(d), k)
    e = generate_lambda(primes[0], primes[1])

    with open('publickeyinfo.txt', 'w') as f1:
        f1.write("# modulus (n)\n")
        f1.write(str(primes[0] * primes[1]) + "\n")
        f1.write("# exponent (e)\n")
        f1.write(str(e) + "\n")

    with open('secretprimes.txt', 'w') as f2:
        f2.write("#p\n")
        f2.write(str(primes[0]) + "\n")
        f2.write("#q\n")
        f2.write(str(primes[1]) + "\n")

    # for i in range(1000):
    #     b = random.randint(1, 1000)
    #     e = random.randint(1, 1000)
    #     m = random.randint(1, 1000)
    #
    #     if modular_exponentiation(b, e, m) != (b ** e) % m:
    #         raise Exception
    # print(euclidean_gcd(7854,4746))
    # k = 20
    # d = 10
    # start_time = time.perf_counter()
    # primes = generate_primes(d, k)
    # e = generate_lambda(primes[0], primes[1])
    # end_time = time.perf_counter()
    # print(primes[0], primes[1])
    # print(primes[0] * primes[1])
    # print(e)
    # elapsed_time = end_time - start_time
    # print("Time taken:", elapsed_time, "seconds")
