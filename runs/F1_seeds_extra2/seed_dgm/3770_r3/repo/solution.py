class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L
        fixed = [False] * L

        # Place forced characters from 'T' constraints.
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    p = i + k
                    if fixed[p]:
                        if word[p] != str2[k]:
                            return ""
                    else:
                        fixed[p] = True
                        word[p] = str2[k]

        # Fill remaining free positions with 'a'.
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'

        # Fix 'F' constraints: each window must differ from str2.
        # Use Z-like check: window equals str2 iff all positions match.
        def matches(i):
            for k in range(m):
                if word[i + k] != str2[k]:
                    return False
            return True

        for i, c in enumerate(str1):
            if c == 'F' and matches(i):
                # Change the rightmost free position in the window.
                for p in range(i + m - 1, i - 1, -1):
                    if not fixed[p]:
                        # Smallest char different from the one str2 requires there.
                        want = str2[p - i]
                        word[p] = 'b' if want == 'a' else 'a'
                        break
                else:
                    return ""

        result = "".join(word)
        # Final verification.
        for i, c in enumerate(str1):
            eq = result[i:i + m] == str2
            if (c == 'T') != eq:
                return ""
        return result
