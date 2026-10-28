from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def bits_of(mask):
            res = []
            v = 0
            while mask:
                if mask & 1:
                    res.append(v)
                mask >>= 1
                v += 1
            return res

        def add(mask, x):
            # mask: bitmask over OR-values; return mask of {v | x : v in mask}
            out = 0
            for v in bits_of(mask):
                out |= 1 << (v | x)
            return out

        # suf[i][c]: bitmask of OR values from choosing c elements from nums[i:]
        suf = [[0] * (k + 1) for _ in range(n + 1)]
        suf[n][0] = 1  # OR value 0 achievable with empty selection
        for i in range(n - 1, -1, -1):
            x = nums[i]
            row, nxt = suf[i], suf[i + 1]
            for c in range(k + 1):
                row[c] = nxt[c]
                if c > 0 and nxt[c - 1]:
                    row[c] |= add(nxt[c - 1], x)

        best = 0
        pre = [0] * (k + 1)
        pre[0] = 1
        for i in range(n + 1):
            # pre currently covers nums[:i]
            if i >= k and pre[k] and suf[i][k]:
                A = bits_of(pre[k])
                B = bits_of(suf[i][k])
                for a in A:
                    for b in B:
                        if a ^ b > best:
                            best = a ^ b
            if i == n:
                break
            x = nums[i]
            new = pre[:]
            for c in range(1, k + 1):
                if pre[c - 1]:
                    new[c] |= add(pre[c - 1], x)
            pre = new
        return best
