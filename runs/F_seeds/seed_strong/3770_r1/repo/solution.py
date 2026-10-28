from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        # Z-function of str2
        z = [0] * m
        z[0] = m
        l = r = 0
        for i in range(1, m):
            if i < r:
                z[i] = min(r - i, z[i - l])
            while i + z[i] < m and str2[z[i]] == str2[i + z[i]]:
                z[i] += 1
            if i + z[i] > r:
                l, r = i, i + z[i]

        word = ['a'] * L
        fixed = [False] * L
        prev = -1
        for i in range(n):
            if str1[i] != 'T':
                continue
            if prev >= 0 and i - prev < m:
                d = i - prev
                # str2[d:] must equal prefix of str2 of length m-d
                if z[d] < m - d:
                    return ""
            for p in range(i, i + m):
                if not fixed[p]:
                    fixed[p] = True
                    word[p] = str2[p - i]
            prev = i

        for i in range(n):
            if str1[i] != 'F':
                continue
            if ''.join(word[i:i + m]) != str2:
                continue
            j = i + m - 1
            while j >= i and fixed[j]:
                j -= 1
            if j < i:
                return ""
            c = 'a' if str2[j - i] != 'a' else 'b'
            word[j] = c

        res = ''.join(word)
        # final verification
        for i in range(n):
            sub = res[i:i + m]
            if str1[i] == 'T' and sub != str2:
                return ""
            if str1[i] == 'F' and sub == str2:
                return ""
        return res
