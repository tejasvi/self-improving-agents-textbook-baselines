class Solution:
    def numberOfWays(self, s: str, t: str, k: int) -> int:
        MOD = 10**9 + 7
        n = len(s)

        # Find all rotations p in [0, n) with rotate(s, p) == t,
        # i.e. (s+s)[p:p+n] == t, via the Z-function on t + '#' + s + s.
        u = t + '#' + s + s
        m = len(u)
        z = [0] * m
        l = r = 0
        for i in range(1, m):
            if i < r:
                z[i] = min(r - i, z[i - l])
            while i + z[i] < m and u[z[i]] == u[i + z[i]]:
                z[i] += 1
            if i + z[i] > r:
                l, r = i, i + z[i]

        off = n + 1
        cnt = 0
        for p in range(n):
            if z[off + p] >= n:
                cnt += 1

        same = 1 if s == t else 0  # rotation by 0 gives t
        nonzero = cnt - same

        # Ways for k steps with each step in {1..n-1} summing to 0 mod n (f)
        # or to a specific nonzero residue mod n (g).
        sign = 1 if k % 2 == 0 else -1
        inv_n = pow(n, MOD - 2, MOD)
        pw = pow(n - 1, k, MOD)
        f = (pw + (n - 1) * sign) % MOD * inv_n % MOD
        g = (pw - sign) % MOD * inv_n % MOD

        return (same * f + nonzero * g) % MOD
