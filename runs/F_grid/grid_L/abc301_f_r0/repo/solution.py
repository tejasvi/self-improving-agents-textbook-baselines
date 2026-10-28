import sys

MOD = 998244353


def solve(S):
    # A[u]: no repeated uppercase so far; u = number of '?'-chosen uppercase
    #       letters, f = number of fixed uppercase letters (all distinct).
    # B: a repeated uppercase pair exists, no lowercase since its completion.
    # C: pair exists and a lowercase has appeared since; uppercase kills it.
    A = [0] * 28
    A[0] = 1
    B = 0
    C = 0
    f = 0
    F = set()
    inv = [0] * 28
    for i in range(1, 28):
        inv[i] = pow(i, MOD - 2, MOD)
    for ch in S:
        if ch == '?':
            m = 26 - f
            newA = [0] * 28
            sAf = 0
            for u in range(28):
                a = A[u]
                if a:
                    newA[u] = 26 * a
                    sAf += a * (f + u)
            for u in range(1, 28):
                a = A[u - 1]
                if a:
                    k = m - (u - 1)
                    if k > 0:
                        newA[u] += a * k
            newA = [x % MOD for x in newA]
            newB = (26 * B + sAf) % MOD
            newC = (26 * B + 26 * C) % MOD
            A, B, C = newA, newB, newC
        elif ch.islower():
            # fixed lowercase
            C = (B + C) % MOD
            B = 0
        else:
            if ch in F:
                B = (B + sum(A)) % MOD
                A = [0] * 28
                C = 0
            else:
                m = 26 - f
                im = inv[m]
                sUf = 0
                newA = [0] * 28
                for u in range(28):
                    a = A[u]
                    if a and u <= m:
                        sUf += a * u
                        newA[u] = a * (m - u) % MOD * im % MOD
                B = (B + sUf % MOD * im) % MOD
                A = newA
                C = 0
                F.add(ch)
                f += 1
    return (sum(A) + B + C) % MOD


def main():
    S = sys.stdin.readline().strip()
    print(solve(S))


if __name__ == "__main__":
    main()
