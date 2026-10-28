from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        w = [''] * L
        fixed = [False] * L
        # Place forced characters from 'T' windows.
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    p = i + k
                    c = str2[k]
                    if fixed[p]:
                        if w[p] != c:
                            return ""
                    else:
                        fixed[p] = True
                        w[p] = c
        # Fill free positions with the smallest letter.
        for p in range(L):
            if not fixed[p]:
                w[p] = 'a'
        # Break every 'F' window that equals str2 by bumping its rightmost free cell.
        for i in range(n):
            if str1[i] == 'F' and ''.join(w[i:i + m]) == str2:
                j = i + m - 1
                while j >= i and fixed[j]:
                    j -= 1
                if j < i:
                    return ""
                w[j] = chr(ord(w[j]) + 1)
        res = ''.join(w)
        # Final verification.
        for i in range(n):
            eq = res[i:i + m] == str2
            if (str1[i] == 'T') != eq:
                return ""
        return res
