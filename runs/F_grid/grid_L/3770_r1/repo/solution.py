class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [''] * L
        covered = [False] * L
        # Forced positions from 'T' constraints.
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    p = i + k
                    covered[p] = True
                    if word[p] == '':
                        word[p] = str2[k]
                    elif word[p] != str2[k]:
                        return ""
        # Free positions default to 'a'.
        for p in range(L):
            if word[p] == '':
                word[p] = 'a'
        # Fix 'F' windows that accidentally equal str2 by changing a
        # rightmost uncovered position (not forced by any 'T') to 'b'.
        for i, c in enumerate(str1):
            if c == 'F' and ''.join(word[i:i + m]) == str2:
                for p in range(i + m - 1, i - 1, -1):
                    if not covered[p]:
                        word[p] = 'b'
                        break
                else:
                    return ""
        return ''.join(word)
