class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = [''] * L
        fixed = [False] * L

        # Place all 'T' constraints.
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    p = i + j
                    if fixed[p]:
                        if word[p] != str2[j]:
                            return ""
                    else:
                        fixed[p] = True
                        word[p] = str2[j]

        # Fill remaining free positions with 'a'.
        for p in range(L):
            if not fixed[p]:
                word[p] = 'a'

        # Handle 'F' constraints: each window must differ from str2.
        for i in range(n):
            if str1[i] == 'F':
                if ''.join(word[i:i + m]) == str2:
                    # Change the rightmost free position in the window to 'b'.
                    j = i + m - 1
                    while j >= i and fixed[j]:
                        j -= 1
                    if j < i:
                        return ""
                    word[j] = 'b'
                    fixed[j] = True  # keep it changed; treated as settled

        return ''.join(word)
