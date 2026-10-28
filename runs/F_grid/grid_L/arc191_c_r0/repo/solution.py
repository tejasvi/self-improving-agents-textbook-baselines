import sys
import random
from math import gcd

def is_prime(n):
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def pollard(n):
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(1, n)
        f = lambda x: (x * x + c) % n
        x = y = random.randrange(2, n)
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n, out):
    if n == 1:
        return
    if is_prime(n):
        out.add(n)
        return
    # small trial division first
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            out.add(p)
            factor(n // p, out)
            return
    d = pollard(n)
    factor(d, out)
    factor(n // d, out)

def solve(N):
    if N == 1:
        return 1, 1
    primes = set()
    factor(N, primes)
    start = 10**17 // N + 1
    k = start
    while True:
        p = k * N + 1
        if is_prime(p):
            # find element of order exactly N
            e = (p - 1) // N
            a = 2
            while True:
                x = pow(a, e, p)
                if x != 1 and all(pow(x, N // q, p) != 1 for q in primes):
                    return x, p
                a += 1
        k += 1

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        N = int(data[i])
        A, M = solve(N)
        out.append(f"{A} {M}")
    sys.stdout.write("\n".join(out) + "\n")

main()
