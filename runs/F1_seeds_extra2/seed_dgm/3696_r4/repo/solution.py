class Solution:
    def countSubstrings(self, s: str) -> int:
        # For each modulus m in 1..9, cnt[m][r] = number of start positions i
        # such that value(s[i..j]) % m == r, for the current end j.
        cnt = {m: [0] * m for m in range(1, 10)}
        total = 0
        for ch in s:
            c = ord(ch) - 48
            # Extend all existing windows by digit c: r -> (10r + c) % m
            for m in range(1, 10):
                old = cnt[m]
                new = [0] * m
                for r in range(m):
                    v = old[r]
                    if v:
                        new[(10 * r + c) % m] += v
                # Add the new window consisting of just c
                new[c % m] += 1
                cnt[m] = new
            if c != 0:
                # Windows ending here whose value is divisible by c
                total += cnt[c][0]
        return total
