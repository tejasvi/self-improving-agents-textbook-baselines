class Solution:
    def countSubstrings(self, s: str) -> int:
        # For each modulus d in 1..9, cnt[d][r] = number of start indices j <= i
        # such that value(s[j..i]) % d == r. Updating for a new digit c is
        # value -> value*10 + c, which is a map on residues mod d.
        cnt = {d: [0] * d for d in range(1, 10)}
        ans = 0
        for ch in s:
            c = ord(ch) - 48
            for d in range(1, 10):
                old = cnt[d]
                new = [0] * d
                for r in range(d):
                    v = old[r]
                    if v:
                        new[(10 * r + c) % d] += v
                new[c % d] += 1
                cnt[d] = new
            if c:
                ans += cnt[c][0]
        return ans
