class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [''] * L
        fixed = [False] * L

        # Apply all 'T' constraints.
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

        # Fill free positions with 'a' (smallest letter).
        for p in range(L):
            if not fixed[p]:
                word[p] = 'a'

        # Enforce 'F' constraints: break any match by bumping the rightmost free position.
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if word[i:i + m] != list(str2):
                continue
            for p in range(i + m - 1, i - 1, -1):
                if not fixed[p]:
                    word[p] = 'b'
                    break
            else:
                return ""

        result = ''.join(word)
        # Final verification for safety.
        for i, c in enumerate(str1):
            match = result[i:i + m] == str2
            if (c == 'T') != match:
                return ""
        return result
