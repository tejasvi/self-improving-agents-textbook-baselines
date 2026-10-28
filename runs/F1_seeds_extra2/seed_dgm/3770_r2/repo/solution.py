class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [None] * L      # None = free position
        fixed = [False] * L
        # Apply all 'T' constraints
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
        # Fill free positions with 'a'
        for p in range(L):
            if word[p] is None:
                word[p] = 'a'
        # Handle 'F' constraints: each window must differ from str2.
        # Changing the last free position in the window to 'b' is the
        # cheapest way to break the match.
        for i, c in enumerate(str1):
            if c != 'F':
                continue
            if word[i:i + m] != list(str2):
                continue
            for p in range(i + m - 1, i - 1, -1):
                if not fixed[p]:
                    fixed[p] = True  # now changed; mark so it's not reused
                    word[p] = 'b'
                    break
            else:
                return ""
        # Final verification
        s = ''.join(word)
        for i, c in enumerate(str1):
            eq = s[i:i + m] == str2
            if (c == 'T') != eq:
                return ""
        return s
