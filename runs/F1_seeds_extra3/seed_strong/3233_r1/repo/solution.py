from typing import *


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        # State: (mask of distinct letters in open segment, changed flag) -> max closed partitions.
        # Mask determines popcount; partitions are additive, so keeping max per state is exact.
        cur = {(0, False): 0}
        for ch in s:
            orig = 1 << (ord(ch) - 97)
            nxt = {}
            for (m, used), p in cur.items():
                # option 1: keep the original character
                options = [orig]
                if not used:
                    # option 2: change this character to any letter
                    # (letters already in mask or new letters; a new letter is best
                    # represented by any bit not in mask, but we must enumerate)
                    options = range(26)
                    options = [1 << c for c in options]
                for x in options:
                    nu = used or (x != orig)
                    if m & x:
                        key, val = (m, nu), p
                    elif bin(m).count("1") < k:
                        key, val = (m | x, nu), p
                    else:
                        key, val = (x, nu), p + 1
                    if nxt.get(key, -1) < val:
                        nxt[key] = val
            cur = nxt
        best = 0
        for (m, used), p in cur.items():
            best = max(best, p + 1)
        return best
