import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] + [int(v) for v in data[1:1 + n]]
    invN = pow(n, MOD - 2, MOD)
    # E[x] = expected future salary when current x; E[x] = invN * sum_{y>x} (A[y] + E[y])
    S = 0
    E = 0
    for x in range(n, -1, -1):
        E = S * invN % MOD
        if x >= 1:
            S = (S + A[x] + E) % MOD
    print(E % MOD)

main()
