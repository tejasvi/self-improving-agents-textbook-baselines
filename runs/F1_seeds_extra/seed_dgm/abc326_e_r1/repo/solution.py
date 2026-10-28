import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E_x = inv_n * sum_{y > x} (A_y + E_y); E_N = 0; answer E_0.
    s = 0
    for x in range(n, 0, -1):
        e = s * inv_n % MOD  # E_x
        s = (s + a[x - 1] + e) % MOD
    ans = s * inv_n % MOD  # E_0
    print(ans)

main()
