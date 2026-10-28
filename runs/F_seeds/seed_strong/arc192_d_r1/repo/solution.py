import sys
from operator import add

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


def solve_prime(p, b):
    # b[i] = v_p(A_i); e_i = v_p(S_i) >= 0, |e_i - e_{i+1}| = b[i], min e_i = 0.
    # Weight of a sequence = p^(sum e_i). Sum over all valid e.
    R = sum(b)
    if R == 0:
        return 1
    pw = [1] * (R + 1)
    for v in range(1, R + 1):
        pw[v] = pw[v - 1] * p % MOD
    # A: zero not yet reached (values >= 1); B: zero reached (values >= 0)
    A = [0] + pw[1:]
    B = [1] + [0] * R
    for bi in b:
        if bi == 0:
            A = [x * y % MOD for x, y in zip(A, pw)]
            B = [x * y % MOD for x, y in zip(B, pw)]
            continue
        nA = [0] * (R + 1)
        nB = [0] * (R + 1)
        # up moves (v -> v+bi)
        nA[bi:] = A[:R + 1 - bi]
        nB[bi:] = B[:R + 1 - bi]
        # down moves (v -> v-bi)
        if R - bi >= 0:
            nA[1:R - bi + 1] = map(add, nA[1:R - bi + 1], A[bi + 1:R + 1])
            nB[0:R - bi + 1] = map(add, nB[0:R - bi + 1], B[bi:R + 1])
        # A -> B when reaching exactly 0
        nB[0] += A[bi]
        A = [x % MOD * y % MOD for x, y in zip(nA, pw)]
        B = [x % MOD * y % MOD for x, y in zip(nB, pw)]
    return sum(B) % MOD


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:n]]
    fac = [factorize(x) for x in a]
    primes = set()
    for f in fac:
        primes.update(f.keys())
    ans = 1
    for p in sorted(primes):
        b = [f.get(p, 0) for f in fac]
        ans = ans * solve_prime(p, b) % MOD
    print(ans)


main()
