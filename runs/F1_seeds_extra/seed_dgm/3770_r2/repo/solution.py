class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [''] * L
        forced = [False] * L

        # Place all forced characters from 'T' constraints.
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

        # Fill remaining free positions with 'a'.
        for p in range(L):
            if not forced[p]:
                word[p] = 'a'

        # Ensure every 'F' window differs from str2.
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            # Check whether window currently equals str2.
            if word[i:i + m] != list(str2):
                continue
            # Change the rightmost free position in the window.
            changed = False
            for j in range(i + m - 1, i - 1, -1):
                if not forced[j]:
                    word[j] = 'b' if str2[j - i] == 'a' else 'a'
                    changed = True
                    break
            if not changed:
                return ""

        return ''.join(word)
