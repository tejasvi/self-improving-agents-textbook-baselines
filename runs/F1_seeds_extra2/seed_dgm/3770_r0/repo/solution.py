class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L  # None = free position
        # Place forced characters from 'T' constraints.
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    p = i + k
                    if word[p] is None:
                        word[p] = str2[k]
                    elif word[p] != str2[k]:
                        return ""
        # Fill free positions with 'a' (smallest).
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'
        # Fix 'F' constraints: for each window that equals str2, change
        # the last free position inside it to 'b' (free positions are never
        # covered by a 'T' window, so this cannot break 'T' constraints).
        forced = [False] * L
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    forced[i + k] = True
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if word[i:i + m] == list(str2):
                for p in range(i + m - 1, i - 1, -1):
                    if not forced[p]:
                        word[p] = 'b'
                        break
                else:
                    return ""
        result = ''.join(word)
        # Final verification.
        for i, c in enumerate(str1):
            match = result[i:i + m] == str2
            if (c == 'T') != match:
                return ""
        return result
