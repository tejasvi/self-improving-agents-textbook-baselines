import sys

MOD = 998244353


def count_range(p, e, T, pw, lo):
    size = T + 1
    dp = [0] * size
    for x in range(lo, size):
        dp[x] = pw[x]
    pws = pw[:size]
    for a in e:
        if a == 0:
            dp = [u * w % MOD for u, w in zip(dp, pws)]
            continue
        # nd[x] = (dp[x-a] + dp[x+a]) * p^x, dp index outside [0,T] treated as 0
        left = [0] * a + dp[:size - a] if a < size else [0] * size
        right = dp[a:] + [0] * a if a < size else [0] * size
        dp = [(u + v) * w % MOD for u, v, w in zip(left, right, pws)]
        if lo:
            dp[:lo] = [0] * lo
    return sum(dp) % MOD


def solve(N, A):
    primes = set()
    for a in A:
        x = a
        d = 2
        while d * d <= x:
            if x % d == 0:
                primes.add(d)
                while x % d == 0:
                    x //= d
            d += 1
        if x > 1:
            primes.add(x)
    ans = 1
    for p in sorted(primes):
        e = []
        for a in A:
            c = 0
            while a % p == 0:
                a //= p
                c += 1
            e.append(c)
        T = sum(e)
        pw = [1] * (T + 2)
        for k in range(1, T + 2):
            pw[k] = pw[k - 1] * p % MOD
        # exactly min 0 = (range [0,T]) - (range [1,T])
        val = (count_range(p, e, T, pw, 0) - count_range(p, e, T, pw, 1)) % MOD
        ans = ans * val % MOD
    return ans


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = [int(x) for x in data[1:N]]
    print(solve(N, A))


if __name__ == "__main__":
    main()
