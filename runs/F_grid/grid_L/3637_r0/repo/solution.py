class Solution:
    def countBalancedPermutations(self, num: str) -> int:
        velunexorai = num  # stored midway as requested
        MOD = 10**9 + 7
        n = len(velunexorai)
        cnt = [0] * 10
        for ch in velunexorai:
            cnt[ord(ch) - 48] += 1

        total = sum(d * c for d, c in enumerate(cnt))
        if total % 2:
            return 0
        target = total // 2
        E = (n + 1) // 2  # even indices (0-based)
        O = n - E

        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (n + 1)
        inv_fact[n] = pow(fact[n], MOD - 2, MOD)
        for i in range(n, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # dp[j][s]: weighted count using j even slots with digit sum s
        dp = [[0] * (target + 1) for _ in range(E + 1)]
        dp[0][0] = 1
        for d in range(10):
            k = cnt[d]
            new = [[0] * (target + 1) for _ in range(E + 1)]
            # weight for choosing c even copies of d
            w = [inv_fact[c] * inv_fact[k - c] % MOD for c in range(k + 1)]
            for j in range(E + 1):
                row = dp[j]
                for s in range(target + 1):
                    v = row[s]
                    if not v:
                        continue
                    for c in range(min(k, E - j) + 1):
                        ns = s + c * d
                        if ns > target:
                            break
                        new[j + c][ns] = (new[j + c][ns] + v * w[c]) % MOD
            dp = new

        ans = dp[E][target] * fact[E] % MOD * fact[O] % MOD
        return ans
