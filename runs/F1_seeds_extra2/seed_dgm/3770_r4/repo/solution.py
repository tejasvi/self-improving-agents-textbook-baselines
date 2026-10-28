class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L
        forced = [False] * L
        # Place forced characters from 'T' constraints.
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
        # Fill free positions with the smallest letter.
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'
        # Break every 'F' window that currently equals str2.
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if word[i:i + m] != list(str2):
                continue
            # Rightmost free position in the window to change (keeps prefix smallest).
            for p in range(i + m - 1, i - 1, -1):
                if not forced[p]:
                    k = str2[p - i]
                    word[p] = 'b' if k == 'a' else 'a'
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
