import sys


def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]), E[N] = 0; answer E[0].
    cur_e = 0  # E[x+1] while iterating
    s = 0      # running sum of (A_y + E_y) over y > x
    for x in range(n - 1, -1, -1):
        s = (s + a[x] + cur_e) % MOD  # y = x+1, A_y = a[x] (0-indexed)
        cur_e = s * inv_n % MOD
    print(cur_e % MOD)


main()
