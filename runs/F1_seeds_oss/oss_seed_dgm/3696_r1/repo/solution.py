class Solution:
    def countSubstrings(self, s: str) -> int:
        # Initialize count arrays for each possible non-zero digit (1..9).
        # cnt_mod[d][r] = number of substrings ending at the previous position
        # whose value modulo d is r.
        cnt_mod = {d: [0] * d for d in range(1, 10)}
        ans = 0
        for ch in s:
            cur = ord(ch) - ord('0')
            # Update cnt_mod for every d using the new digit.
            for d in range(1, 10):
                prev = cnt_mod[d]
                new = [0] * d
                # Extend existing substrings ending at previous index.
                if any(prev):  # small optimisation, but loop anyway
                    for r in range(d):
                        cnt = prev[r]
                        if cnt:
                            new_r = (r * 10 + cur) % d
                            new[new_r] += cnt
                # Add the substring consisting of just the current digit.
                new[cur % d] += 1
                cnt_mod[d] = new
            # If current digit is non-zero, add substrings whose last digit equals cur
            # and whose value is divisible by cur (i.e., remainder 0 modulo cur).
            if cur != 0:
                ans += cnt_mod[cur][0]
        return ans
