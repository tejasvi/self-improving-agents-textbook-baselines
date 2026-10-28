import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [0] + [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]); E[N] = 0
    suffix = 0  # sum_{y>x} (A_y + E[y])
    E0 = 0
    for x in range(n, -1, -1):
        e = suffix * inv_n % MOD
        if x == 0:
            E0 = e
        else:
            suffix = (suffix + A[x] + e) % MOD
    print(E0)

main()
