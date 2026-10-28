import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    p = [int(x) for x in data[2:2 + n]]
    m = n - k + 1

    tree = [0] * (n + 1)

    def add(i, d):
        while i <= n:
            tree[i] += d
            i += i & (-i)

    def query(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    # Total initial inversion count I
    total_inv = 0
    for idx in range(n):
        x = p[idx]
        total_inv += idx - query(x)  # earlier elements greater than x
        add(x, 1)

    # Reset BIT for sliding window
    tree = [0] * (n + 1)

    def add2(i, d):
        while i <= n:
            tree[i] += d
            i += i & (-i)

    def query2(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    inv = 0
    cnt = 0
    for idx in range(k):
        x = p[idx]
        inv += cnt - query2(x)
        add2(x, 1)
        cnt += 1
    s2 = inv
    for i in range(1, m):
        # remove leftmost p[i-1]: it is left of all others
        x = p[i - 1]
        inv -= query2(x - 1)
        add2(x, -1)
        cnt -= 1
        # add rightmost p[i+k-1]: it is right of all others
        y = p[i + k - 1]
        inv += cnt - query2(y)
        add2(y, 1)
        cnt += 1
        s2 += inv

    inv4 = pow(4, MOD - 2, MOD)
    invm = pow(m, MOD - 2, MOD)
    ans = (k * (k - 1) % MOD * inv4 + total_inv % MOD - s2 % MOD * invm) % MOD
    print(ans % MOD)


main()
