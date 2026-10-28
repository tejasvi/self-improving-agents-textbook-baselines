import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(v) for v in data[1:1 + n]]
    invn = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]),  E[N] = 0, answer E[0]
    T = 0  # sum over y > x of (A_y + E[y])
    E = 0
    for x in range(n, -1, -1):
        E = T * invn % MOD  # E[x]
        if x >= 1:
            T = (T + A[x - 1] + E) % MOD
    print(E % MOD)

main()
