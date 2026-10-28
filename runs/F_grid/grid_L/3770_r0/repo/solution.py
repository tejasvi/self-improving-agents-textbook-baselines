class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L    # None = free position
        forced = [False] * L

        # Apply all 'T' constraints
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

        # Fill free positions with 'a' (smallest letter)
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'

        def matches(i):
            for k in range(m):
                if word[i + k] != str2[k]:
                    return False
            return True

        # Fix 'F' constraints greedily: change the rightmost free position
        # in the window to the smallest letter different from str2's letter.
        for i, c in enumerate(str1):
            if c != 'F' or not matches(i):
                continue
            j = -1
            for p in range(i + m - 1, i - 1, -1):
                if not forced[p]:
                    j = p
                    break
            if j < 0:
                return ""
            want = str2[j - i]
            word[j] = 'b' if want == 'a' else 'a'

        # Final verification
        for i, c in enumerate(str1):
            if c == 'T' and not matches(i):
                return ""
            if c == 'F' and matches(i):
                return ""
        return "".join(word)
