class Solution:
    def countSubstrings(self, s: str) -> int:
        # For each modulus m in 1..9, cnt[m][r] = number of substrings ending at
        # the current position whose value is congruent to r (mod m).
        # Extending by digit c: value' = 10*value + c.
        cnt = {m: [0] * m for m in range(1, 10)}
        total = 0
        for ch in s:
            c = ord(ch) - 48
            for m in range(1, 10):
                old = cnt[m]
                new = [0] * m
                for r in range(m):
                    v = old[r]
                    if v:
                        new[(10 * r + c) % m] += v
                new[c % m] += 1  # substring consisting of just this digit
                cnt[m] = new
            if c:
                total += cnt[c][0]
        return total
