import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]), E[N] = 0
    # Process x from N down to 0, maintaining T = sum_{y>x} (A_y + E[y]).
    T = 0
    e = 0
    for x in range(n, -1, -1):
        e = T * inv_n % MOD
        if x >= 1:
            T = (T + a[x - 1] + e) % MOD
    print(e % MOD)

main()
