import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]), E[N] = 0
    acc = 0  # sum over y > x of (A_y + E_y)
    e = 0
    for x in range(n, -1, -1):
        e = acc * inv_n % MOD  # E[x]
        if x >= 1:
            acc = (acc + A[x - 1] + e) % MOD
    print(e % MOD)

main()
