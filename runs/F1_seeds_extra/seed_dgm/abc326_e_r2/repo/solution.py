import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y > x} (A_y + E[y]), E[N] = 0
    # Process x from N down to 0, maintaining S = sum_{y > x} (A_y + E[y]).
    S = 0
    e = 0
    for x in range(n, 0, -1):
        # E[x] = S / N (E[N] = 0 since S = 0 at start)
        e = S * inv_n % MOD
        S = (S + a[x - 1] + e) % MOD
    # E[0]
    ans = S * inv_n % MOD
    print(ans)

main()
