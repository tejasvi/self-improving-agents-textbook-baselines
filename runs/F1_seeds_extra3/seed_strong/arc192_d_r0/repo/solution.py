import sys

MOD = 998244353


def factorize(n):
    res = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            res[d] = res.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        res[n] = res.get(n, 0) + 1
    return res


def solve(n, A):
    # per prime: list of (edge index j (1-based), exponent d)
    edges = {}
    for j, a in enumerate(A, start=1):
        for r, d in factorize(a).items():
            edges.setdefault(r, []).append((j, d))

    total = 1
    for r, lst in edges.items():
        # DP over x = e - prefix_min >= 0; dp[x] = sum of weights
        dp = [1]          # x = 0 at position 1
        w_pos = 0         # positions 1..w_pos already weighted
        for j, d in lst:
            # positions w_pos+1..j currently have x (dp), weight r^x each
            g = j - w_pos
            if g > 0:
                base = pow(r, g, MOD)
                cur = 1
                for x in range(len(dp)):
                    if dp[x]:
                        dp[x] = dp[x] * cur % MOD
                    cur = cur * base % MOD
            w_pos = j
            # drop penalties: going down from x < d costs r^((d-x)*j)
            R = len(dp)
            new = [0] * (R + d)
            # up move: x -> x + d
            for x in range(R):
                new[x + d] += dp[x]
            # down move
            pen = [pow(r, (d - x) * j, MOD) for x in range(d)]
            low = 0
            for x in range(min(d, R)):
                low = (low + dp[x] * pen[x]) % MOD
            for x in range(d, R):
                new[x - d] += dp[x]
            new[0] += low
            dp = [v % MOD for v in new]
            # trim trailing zeros is unnecessary for correctness
        # final positions w_pos+1..n
        g = n - w_pos
        base = pow(r, g, MOD)
        cur = 1
        s = 0
        for x in range(len(dp)):
            s += dp[x] * cur
            cur = cur * base % MOD
        total = total * (s % MOD) % MOD
    return total


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(v) for v in data[1:n]]
    print(solve(n, A) % MOD)


if __name__ == "__main__":
    main()
