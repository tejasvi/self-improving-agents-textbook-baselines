import sys


def is_prime(n):
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for q in small:
        if n % q == 0:
            return n == q
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


def prime_factors(n):
    fs = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fs.append(n)
    return fs


def solve(N):
    if N == 1:
        return 2, 1
    qs = prime_factors(N)
    k = 1
    a = 2
    while True:
        p = k * N + 1
        k += 1
        if p > 10**18:
            raise RuntimeError("no prime found")
        if not is_prime(p):
            continue
        # try a few bases for a
        for base in range(2, 200):
            A = pow(base, (p - 1) // N, p)
            if all(pow(A, N // q, p) != 1 for q in qs):
                return A, p


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        N = int(data[i])
        A, M = solve(N)
        out.append(f"{A} {M}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
