class Solution:
    def countSubstrings(self, s: str) -> int:
        # cnt[d][r]: number of start positions i (<= current end) such that
        # value(s[i..j]) % d == r, for d in 1..9.
        cnt = {d: [0] * d for d in range(1, 10)}
        ans = 0
        for ch in s:
            c = ord(ch) - 48
            new = {}
            for d in range(1, 10):
                old = cnt[d]
                nw = [0] * d
                for m in range(d):
                    v = old[m]
                    if v:
                        nw[(m * 10 + c) % d] += v
                nw[c % d] += 1  # substring starting at current position
                new[d] = nw
                if c and c == d:
                    ans += nw[0]
            cnt = new
        return ans
