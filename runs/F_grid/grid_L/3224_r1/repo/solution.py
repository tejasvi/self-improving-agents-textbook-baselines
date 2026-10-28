from typing import List


class Solution:
    def numberOfSequence(self, n: int, sick: List[int]) -> int:
        MOD = 10**9 + 7
        total = n - len(sick)  # number of healthy children
        # factorials and inverse factorials
        fact = [1] * (total + 1)
        for i in range(1, total + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv = [1] * (total + 1)
        inv[total] = pow(fact[total], MOD - 2, MOD)
        for i in range(total, 0, -1):
            inv[i - 1] = inv[i] * i % MOD

        # Multinomial coefficient for interleaving the gaps
        result = fact[total]
        gaps = [sick[0], n - 1 - sick[-1]]
        for i in range(1, len(sick)):
            gaps.append(sick[i] - sick[i - 1] - 1)
        for g in gaps:
            result = result * inv[g] % MOD

        # Each interior gap (both ends infected) has 2^(g-1) orderings
        for i in range(1, len(sick)):
            g = sick[i] - sick[i - 1] - 1
            if g > 0:
                result = result * pow(2, g - 1, MOD) % MOD
        return result
