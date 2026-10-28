class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[d][r]: number of start positions i (<= current end) such that
        # value(s[i..j]) % d == r, for d in 1..9.
        cnt = [[0] * d for d in range(10)]
        # Precompute transitions: for modulus d and digit c, r -> (10r + c) % d
        trans = [[[(10 * r + c) % d for r in range(d)] for c in range(10)]
                 for d in range(10)]
        ans = 0
        for ch in s:
            c = ord(ch) - 48
            for d in range(1, 10):
                old = cnt[d]
                t = trans[d][c]
                new = [0] * d
                for r in range(d):
                    v = old[r]
                    if v:
                        new[t[r]] += v
                new[c % d] += 1  # substring starting at this position
                cnt[d] = new
            if c:
                ans += cnt[c][0]
        return ans
