import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [0] + [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]),  E[N] = 0, answer E[0]
    T = 0
    E = 0
    for x in range(n, -1, -1):
        E = T * inv_n % MOD
        if x >= 1:
            T = (T + A[x] + E) % MOD
    print(E)

main()
