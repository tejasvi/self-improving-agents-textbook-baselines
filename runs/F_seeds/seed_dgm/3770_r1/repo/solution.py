class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L
        forced = [False] * L
        # Apply T constraints
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
        # Fill free positions with 'a'
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'
        # Fix F constraints greedily
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if word[i:i + m] != list(str2):
                continue
            # Find last free position in window to change
            j = -1
            for p in range(i + m - 1, i - 1, -1):
                if not forced[p]:
                    j = p
                    break
            if j == -1:
                return ""
            word[j] = 'b' if str2[j - i] == 'a' else 'a'
        result = ''.join(word)
        # Verify
        for i, c in enumerate(str1):
            sub = result[i:i + m]
            if c == 'T' and sub != str2:
                return ""
            if c == 'F' and sub == str2:
                return ""
        return result
