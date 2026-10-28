import sys


def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # f(x) = (1/N) * sum_{y > x} (A_y + f(y)), f(N) = 0; answer f(0).
    # Process x from N down to 0 with running suffix sum s = sum_{y > x} (A_y + f(y)).
    s = 0
    fx = 0
    for x in range(n, 0, -1):
        # f(x) for x = n is 0 (s == 0 here)
        fx = s * inv_n % MOD
        s = (s + a[x - 1] + fx) % MOD
    ans = s * inv_n % MOD
    print(ans)


main()
