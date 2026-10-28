class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L      # None = not yet determined
        forced = [False] * L
        # Place characters required by 'T' constraints.
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    p = i + k
                    if forced[p]:
                        if word[p] != str2[k]:
                            return ""
                    else:
                        forced[p] = True
                        word[p] = str2[k]
        # Fill remaining positions with the smallest letter.
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'
        # Break every 'F' window that equals str2 by changing its last free position.
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if word[i:i + m] == list(str2):
                for p in range(i + m - 1, i - 1, -1):
                    if not forced[p]:
                        word[p] = 'b' if word[p] == 'a' else 'a'
                        break
                else:
                    return ""
        s = ''.join(word)
        # Final verification of all constraints.
        for i, c in enumerate(str1):
            if c == 'T' and s[i:i + m] != str2:
                return ""
            if c == 'F' and s[i:i + m] == str2:
                return ""
        return s
