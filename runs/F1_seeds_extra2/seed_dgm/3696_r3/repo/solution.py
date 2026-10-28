class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[d][r] = number of start positions j (<= current i) such that
        # value(s[j..i]) % d == r, for d in 1..9.
        cnt = [None] + [[0] * d for d in range(1, 10)]
        ans = 0
        for ch in s:
            c = ord(ch) - 48
            for d in range(1, 10):
                old = cnt[d]
                new = [0] * d
                for r in range(d):
                    v = old[r]
                    if v:
                        new[(r * 10 + c) % d] += v
                new[c % d] += 1  # substring starting at current position
                cnt[d] = new
            if c:
                ans += cnt[c][0]
        return ans
