import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(v) for v in data[1:1 + n]]
    invN = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]),  E[N] = 0, answer E[0]
    S = 0
    E = 0
    for x in range(n, -1, -1):
        E = S * invN % MOD
        if x >= 1:
            S = (S + A[x - 1] + E) % MOD
    print(E)

main()
