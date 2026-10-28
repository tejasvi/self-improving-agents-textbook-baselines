import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [0] + [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = expected future salary when current value is x
    # E[x] = inv_n * sum_{y > x} (A[y] + E[y]),  E[N] = 0
    S = 0  # sum_{y > x} (A[y] + E[y])
    E = 0
    for x in range(n, -1, -1):
        E = S * inv_n % MOD
        if x >= 1:
            S = (S + A[x] + E) % MOD
    print(E % MOD)

main()
