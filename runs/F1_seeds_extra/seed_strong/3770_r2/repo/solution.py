from typing import *


class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = ['a'] * L
        fixed = bytearray(L)
        maxend = 0  # fixed positions >= current T start are contiguous up to maxend
        for i in range(n):
            if str1[i] != 'T':
                continue
            e = i + m
            ov_end = min(maxend, e)
            if ov_end > i:
                if word[i:ov_end] != list(str2[:ov_end - i]):
                    return ""
            if e > maxend:
                start = max(maxend, i)
                word[start:e] = list(str2[start - i:])
                fixed[start:e] = b'\x01' * (e - start)
                maxend = e
        # Fix F windows
        for i in range(n):
            if str1[i] != 'F':
                continue
            if word[i:i + m] != list(str2):
                continue
            # find rightmost free position in window
            j = i + m - 1
            while j >= i and fixed[j]:
                j -= 1
            if j < i:
                return ""
            c = str2[j - i]
            word[j] = 'a' if c != 'a' else 'b'
            fixed[j] = 1  # keep it as chosen; it is not forced but now set
        return ''.join(word)
