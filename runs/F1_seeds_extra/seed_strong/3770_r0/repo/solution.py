from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        # Z-function of str2 (for consistency checks between overlapping T windows)
        z = [0] * m
        if m > 0:
            z[0] = m
        l = r = 0
        for i in range(1, m):
            if i < r:
                z[i] = min(r - i, z[i - l])
            while i + z[i] < m and str2[z[i]] == str2[i + z[i]]:
                z[i] += 1
            if i + z[i] > r:
                l, r = i, i + z[i]

        word = [None] * L
        free = [True] * L
        prev = -1
        for i in range(n):
            if str1[i] != 'T':
                continue
            if prev >= 0 and prev + m > i:
                # overlap with latest T window at prev: need str2[i-prev:] == str2[:prev+m-i]
                d = i - prev
                if z[d] < prev + m - i:
                    return ""
            start = i if prev < 0 else max(i, prev + m)
            for x in range(start, i + m):
                word[x] = str2[x - i]
                free[x] = False
            prev = i
        # lastFree[x] = largest free index <= x, or -1
        lastFree = [-1] * L
        cur = -1
        for x in range(L):
            if free[x]:
                cur = x
            lastFree[x] = cur
        for x in range(L):
            if word[x] is None:
                word[x] = 'a'
        for i in range(n):
            if str1[i] != 'F':
                continue
            if ''.join(word[i:i + m]) == str2:
                j = lastFree[i + m - 1]
                if j < i:
                    return ""
                c = 'a' if str2[j - i] != 'a' else 'b'
                word[j] = c
        return ''.join(word)
