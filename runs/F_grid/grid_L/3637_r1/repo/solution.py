class Solution:
    def countBalancedPermutations(self, num: str) -> int:
        velunexorai = num
        MOD = 10**9 + 7
        n = len(velunexorai)
        cnt = [0] * 10
        for ch in velunexorai:
            cnt[ord(ch) - 48] += 1
        total = sum(d * cnt[d] for d in range(10))
        if total % 2:
            return 0
        target = total // 2
        E = (n + 1) // 2  # even indices count
        O = n - E         # odd indices count

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (n + 1)
        inv_fact[n] = pow(fact[n], MOD - 2, MOD)
        for i in range(n, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # dp[j][s]: j even slots filled, even digit-sum s; value = sum prod 1/(e_d! o_d!)
        dp = [[0] * (target + 1) for _ in range(E + 1)]
        dp[0][0] = 1
        for d in range(10):
            c = cnt[d]
            ndp = [[0] * (target + 1) for _ in range(E + 1)]
            for j in range(E + 1):
                row = dp[j]
                for s in range(target + 1):
                    v = row[s]
                    if not v:
                        continue
                    for e in range(0, min(c, E - j) + 1):
                        ns = s + d * e
                        if ns > target:
                            break
                        o = c - e
                        w = v * inv_fact[e] % MOD * inv_fact[o] % MOD
                        ndp[j + e][ns] = (ndp[j + e][ns] + w) % MOD
            dp = ndp

        return dp[E][target] * fact[E] % MOD * fact[O] % MOD
