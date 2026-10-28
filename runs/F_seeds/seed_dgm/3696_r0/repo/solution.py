class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[d][r] = number of start indices i <= j such that
        # value(s[i..j]) mod d == r, for the current end j.
        cnt = {d: [0] * d for d in range(1, 10)}
        ans = 0
        for ch in s:
            c = ord(ch) - 48
            # Extend every existing substring by digit c, and add the new
            # substring starting at j (value c).
            for d in range(1, 10):
                old = cnt[d]
                new = [0] * d
                for r in range(d):
                    if old[r]:
                        new[(r * 10 + c) % d] += old[r]
                new[c % d] += 1
                cnt[d] = new
            if c != 0:
                ans += cnt[c][0]
        return ans
