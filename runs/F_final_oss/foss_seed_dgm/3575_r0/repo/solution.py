from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Prefix DP: prefix[i][c] = set of OR values when selecting c elements from nums[0..i]
        # with the i-th element being selected as the c-th element (i.e., included)
        prefix = [[set() for _ in range(k + 1)] for _ in range(n)]
        for i in range(n):
            prefix[i][1].add(nums[i])
        for i in range(n):
            # we can only select at most i+1 elements ending at i
            max_c = min(k, i + 1)
            for c in range(2, max_c + 1):
                cur_set = set()
                # combine any selection of c-1 elements that ends before i with nums[i]
                for j in range(i):
                    if prefix[j][c - 1]:
                        for val in prefix[j][c - 1]:
                            cur_set.add(val | nums[i])
                prefix[i][c] = cur_set
        # Suffix DP: suffix[i][c] = set of OR values when selecting c elements from nums[i:]
        suffix = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        suffix[n][0].add(0)
        for i in range(n - 1, -1, -1):
            suffix[i][0].add(0)
            for c in range(1, k + 1):
                without = suffix[i + 1][c]
                with_set = set()
                for val in suffix[i + 1][c - 1]:
                    with_set.add(val | nums[i])
                suffix[i][c] = without.union(with_set)
        ans = 0
        for p in range(n):
            if k <= p + 1 and (n - p - 1) >= k:
                for or1 in prefix[p][k]:
                    for or2 in suffix[p + 1][k]:
                        ans = max(ans, or1 ^ or2)
        return ans
