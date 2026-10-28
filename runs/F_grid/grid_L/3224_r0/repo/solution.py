from typing import List


class Solution:
    def numberOfSequence(self, n: int, sick: List[int]) -> int:
        MOD = 10 ** 9 + 7
        total = n - len(sick)

        fact = [1] * (total + 1)
        for i in range(1, total + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (total + 1)
        inv_fact[total] = pow(fact[total], MOD - 2, MOD)
        for i in range(total, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # Multinomial coefficient over all gaps (edge and interior)
        gaps = []
        if sick[0] > 0:
            gaps.append(sick[0])
        if sick[-1] < n - 1:
            gaps.append(n - 1 - sick[-1])
        for i in range(len(sick) - 1):
            gaps.append(sick[i + 1] - sick[i] - 1)

        result = fact[total]
        for m in gaps:
            result = result * inv_fact[m] % MOD

        # Interior gaps can be filled from either end: factor 2^(m-1)
        for i in range(len(sick) - 1):
            m = sick[i + 1] - sick[i] - 1
            if m > 0:
                result = result * pow(2, m - 1, MOD) % MOD
        return result
