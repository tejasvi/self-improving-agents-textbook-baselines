class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        word = ['?'] * L
        fixed = [False] * L  # positions forced by T constraints

        # Apply T constraints
        for i, ch in enumerate(str1):
            if ch == 'T':
                for j in range(m):
                    pos = i + j
                    c = str2[j]
                    if word[pos] == '?':
                        word[pos] = c
                        fixed[pos] = True
                    elif word[pos] != c:
                        # conflict
                        return ""
                    else:
                        fixed[pos] = True  # already same, but still forced
        # Fill remaining positions with 'a' (lexicographically smallest)
        for idx in range(L):
            if word[idx] == '?':
                word[idx] = 'a'

        # Helper to check if a window matches str2 exactly
        def window_matches(start: int) -> bool:
            for j in range(m):
                if word[start + j] != str2[j]:
                    return False
            return True

        # Process F windows to ensure they differ from str2
        for i, ch in enumerate(str1):
            if ch == 'F':
                if not window_matches(i):
                    continue  # already satisfied
                # Need to introduce a mismatch in this window
                changed = False
                # Prefer rightmost position that is not fixed by T
                for pos in range(i + m - 1, i - 1, -1):
                    if fixed[pos]:
                        continue
                    # current character equals str2[pos - i] (since window matches)
                    required = str2[pos - i]
                    # Choose smallest character different from required
                    new_char = 'a' if required != 'a' else 'b'
                    word[pos] = new_char
                    changed = True
                    break
                if not changed:
                    # No mutable position -> impossible
                    return ""
        return ''.join(word)
