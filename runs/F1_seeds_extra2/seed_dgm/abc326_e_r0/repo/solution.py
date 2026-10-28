import sys


def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]); process x from N down to 0.
    T = 0  # sum over y > x of (A_y + E[y])
    E = 0
    for x in range(n, -1, -1):
        E = T * inv_n % MOD
        if x >= 1:
            T = (T + A[x - 1] + E) % MOD
    print(E % MOD)


main()
