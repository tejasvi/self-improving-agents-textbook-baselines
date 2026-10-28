class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[m][r] = number of substrings ending at the current position
        # whose value is congruent to r modulo m.
        cnt = [None] + [[0] * m for m in range(1, 10)]
        ans = 0
        for ch in s:
            c = ord(ch) - 48
            for m in range(1, 10):
                old = cnt[m]
                new = [0] * m
                for r in range(m):
                    v = old[r]
                    if v:
                        new[(10 * r + c) % m] += v
                new[c % m] += 1  # substring starting at this position
                cnt[m] = new
            if c:
                ans += cnt[c][0]
        return ans
