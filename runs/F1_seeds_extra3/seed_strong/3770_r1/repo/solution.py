from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L      # None = free
        fixed = [False] * L
        # Place all 'T' windows.
        for i, c in enumerate(str1):
            if c == 'T':
                for j in range(m):
                    p = i + j
                    if fixed[p]:
                        if word[p] != str2[j]:
                            return ""
                    else:
                        fixed[p] = True
                        word[p] = str2[j]
        # Fill free cells with 'a' (smallest) by default.
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'
        # Fix 'F' windows that accidentally equal str2.
        s2 = list(str2)
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if word[i:i + m] != s2:
                continue
            # Find last free position in the window.
            j = i + m - 1
            while j >= i and fixed[j]:
                j -= 1
            if j < i:
                return ""  # window fully fixed and equal to str2
            want = 'b' if str2[j - i] == 'a' else 'a'
            word[j] = want
        return "".join(word)
