from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L
        forced = [False] * L
        for i, c in enumerate(str1):
            if c == 'T':
                for j in range(m):
                    p = i + j
                    if forced[p]:
                        if word[p] != str2[j]:
                            return ""
                    else:
                        forced[p] = True
                        word[p] = str2[j]
        for p in range(L):
            if not forced[p]:
                word[p] = 'a'
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if ''.join(word[i:i + m]) != str2:
                continue
            # find rightmost free position in window
            k = i + m - 1
            while k >= i and forced[k]:
                k -= 1
            if k < i:
                return ""
            word[k] = 'b'
        return ''.join(word)
