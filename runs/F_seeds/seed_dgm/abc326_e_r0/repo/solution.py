import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [0] + [int(v) for v in data[1:1 + n]]  # 1-indexed
    inv_n = pow(n, MOD - 2, MOD)
    # E_x = (1/N) * sum_{y>x} (A_y + E_y), E_N = 0; answer E_0
    suffix = 0
    e = 0
    for x in range(n, -1, -1):
        e = suffix * inv_n % MOD
        if x >= 1:
            suffix = (suffix + a[x] + e) % MOD
    print(e % MOD)

main()
