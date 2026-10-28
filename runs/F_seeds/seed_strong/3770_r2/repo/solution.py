from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = bytearray(L)           # 0 = unassigned
        s2 = str2.encode()
        end = 0                       # word[0:end] is fully assigned by T windows
        for i in range(n):
            if str1[i] != 'T':
                continue
            if i + m > end:
                # overlap part must match
                if end > i:
                    if word[i:end] != s2[:end - i]:
                        return ""
                if end > i:
                    word[end:i + m] = s2[end - i:]
                else:
                    word[i:i + m] = s2
                end = i + m
            else:
                if word[i:i + m] != s2:
                    return ""
        # positions not assigned by T are free
        free = bytearray(L)
        for p in range(L):
            if word[p] == 0:
                free[p] = 1
                word[p] = ord('a')
        for i in range(n):
            if str1[i] != 'F':
                continue
            if word[i:i + m] == s2:
                p = free.rfind(1, i, i + m)
                if p == -1:
                    return ""
                c = ord('a') if s2[p - i] != ord('a') else ord('b')
                word[p] = c
                free[p] = 0
        return word.decode()
