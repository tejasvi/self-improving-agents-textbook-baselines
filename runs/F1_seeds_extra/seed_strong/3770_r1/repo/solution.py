from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L  # None = free position (not forced by any 'T')
        for i, c in enumerate(str1):
            if c == 'T':
                for j in range(m):
                    p = i + j
                    w = word[p]
                    if w is None:
                        word[p] = str2[j]
                    elif w != str2[j]:
                        return ""
        # Fill free positions with 'a' by default; free positions lie in no 'T' window.
        cur = ['a' if ch is None else ch for ch in word]
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if cur[i:i + m] != list(str2):
                continue  # already differs from str2
            # Window matches; change rightmost free position in it.
            j = m - 1
            while j >= 0 and word[i + j] is not None:
                j -= 1
            if j < 0:
                return ""  # fully forced window equal to str2
            p = i + j
            cur[p] = 'a' if str2[j] != 'a' else 'b'
            word[p] = cur[p]  # mark as fixed so it isn't reused
        return "".join(cur)
