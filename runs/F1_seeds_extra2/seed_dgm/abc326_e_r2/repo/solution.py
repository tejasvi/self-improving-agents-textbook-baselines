import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] + [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = expected future payout from state x
    # E[x] = inv_n * sum_{y>x} (A[y] + E[y])
    S = 0  # suffix sum of (A[y] + E[y]) for y > x
    E = 0
    for x in range(n, -1, -1):
        E = S * inv_n % MOD
        if x >= 1:
            S = (S + A[x] + E) % MOD
    print(E % MOD)

main()
