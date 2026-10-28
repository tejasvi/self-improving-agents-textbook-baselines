import sys

MOD = 998244353


def factorize(x):
    res = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            res[d] = res.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        res[x] = res.get(x, 0) + 1
    return res


def step(vec, a, pw, S):
    # new[h] = pw[h] * (vec[h-a] + vec[h+a]) for a>0; pw[h]*vec[h] for a==0
    if a == 0:
        return [x * w % MOD for x, w in zip(vec, pw)]
    up = [0] * a + vec[:S + 1 - a]
    down = vec[a:] + [0] * a
    return [(x + y) * w % MOD for x, y, w in zip(up, down, pw)]


def solve_prime(p, a):
    # a: list of v_p(A_i), i = 0..N-2 (0-indexed steps); N = len(a)+1
    n = len(a) + 1
    S = sum(a)
    pw = [1] * (S + 1)
    for h in range(1, S + 1):
        pw[h] = pw[h - 1] * p % MOD

    # Left: L[q] for positions q (0-indexed 0..n-1)
    L = [0] * n
    L[0] = 1
    Fs = [0] + pw[1:]  # strict walk ending at position 0
    for j in range(n - 1):
        aj = a[j]
        L[j + 1] = Fs[aj] if aj > 0 else 0
        if j + 1 < n - 1:
            Fs = step(Fs, aj, pw, S)
            Fs[0] = 0

    # Right: R[q]
    R = [0] * n
    R[n - 1] = 1
    Bk = pw[:]  # position n-1
    for q in range(n - 2, -1, -1):
        aq = a[q]
        R[q] = Bk[aq] if aq > 0 else Bk[0]
        if q > 0:
            Bk = step(Bk, aq, pw, S)

    total = 0
    for q in range(n):
        total = (total + L[q] * R[q]) % MOD
    return total


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:n]]
    primes = {}
    for x in A:
        for p in factorize(x):
            primes.setdefault(p, None)
    ans = 1
    for p in primes:
        a = []
        for x in A:
            c = 0
            while x % p == 0:
                x //= p
                c += 1
            a.append(c)
        ans = ans * solve_prime(p, a) % MOD
    print(ans)


if __name__ == "__main__":
    main()
