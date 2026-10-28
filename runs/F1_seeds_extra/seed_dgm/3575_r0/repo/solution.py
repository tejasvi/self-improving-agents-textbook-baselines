from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        # All values < 2^7, so OR values lie in [0, 128).
        # A set of OR values is stored as a 128-bit integer mask.
        B = 128
        n = len(nums)
        byte_tabs = {}

        def or_tab(v):
            # tab[pos][byte] = mask of {x | v : x in bits of byte shifted by 8*pos}
            if v in byte_tabs:
                return byte_tabs[v]
            tab = []
            for pos in range(16):
                row = [0] * 256
                for b in range(1, 256):
                    m = 0
                    for t in range(8):
                        if b >> t & 1:
                            x = pos * 8 + t
                            m |= 1 << (x | v)
                    row[b] = m
                tab.append(row)
            byte_tabs[v] = tab
            return tab

        def apply(tab, mask):
            out = 0
            pos = 0
            while mask:
                b = mask & 0xFF
                if b:
                    out |= tab[pos][b]
                mask >>= 8
                pos += 1
            return out

        def build(seq):
            # res[i][j]: mask of OR values of j-element subsets of seq[:i]
            res = [[0] * (k + 1) for _ in range(n + 1)]
            res[0][0] = 1  # OR value 0 reachable with empty set
            cur = [0] * (k + 1)
            cur[0] = 1
            for i, v in enumerate(seq):
                tab = or_tab(v)
                new = cur[:]
                for j in range(1, k + 1):
                    if cur[j - 1]:
                        new[j] = cur[j] | apply(tab, cur[j - 1])
                cur = new
                res[i + 1] = cur[:]
            return res

        pre = build(nums)
        suf = build(nums[::-1])  # suf[m][j]: j-subsets of last m elements

        def bits(mask):
            out = []
            x = 0
            while mask:
                if mask & 1:
                    out.append(x)
                mask >>= 1
                x += 1
            return out

        best = 0
        for i in range(k, n - k + 1):
            L = pre[i][k]
            R = suf[n - i][k]
            if not L or not R:
                continue
            lb = bits(L)
            rb = bits(R)
            for a in lb:
                for b in rb:
                    if a ^ b > best:
                        best = a ^ b
        return best
