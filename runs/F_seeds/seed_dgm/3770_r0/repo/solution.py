class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L
        fixed = [False] * L

        # Place forced characters from 'T' constraints.
        for i, c in enumerate(str1):
            if c == 'T':
                for j in range(m):
                    p = i + j
                    if fixed[p]:
                        if word[p] != str2[j]:
                            return ""
                    else:
                        fixed[p] = True
                        word[p] = str2[j]

        # Fill remaining free positions with the smallest letter.
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'

        def matches(i):
            for j in range(m):
                if word[i + j] != str2[j]:
                    return False
            return True

        # Break every 'F' window that equals str2 by changing its rightmost free slot.
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if not matches(i):
                continue
            changed = False
            for j in range(m - 1, -1, -1):
                p = i + j
                if not fixed[p]:
                    # word[p] is 'a' here, and str2[j] must be 'a' since the window matches.
                    word[p] = 'b'
                    changed = True
                    break
            if not changed:
                return ""

        result = "".join(word)
        # Final verification.
        for i, c in enumerate(str1):
            sub = result[i:i + m]
            if c == 'T' and sub != str2:
                return ""
            if c == 'F' and sub == str2:
                return ""
        return result
