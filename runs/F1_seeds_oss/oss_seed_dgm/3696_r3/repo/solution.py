class Solution:
    def countSubstrings(self, s: str) -> int:
        # We need to count substrings where the integer value is divisible by its non-zero last digit.
        # For each possible divisor d (1..9) we maintain counts of remainders of all substrings
        # ending at the current position modulo d. When we append a new digit x, a substring's
        # remainder updates as (old_rem * 10 + x) % d. We also start a new substring consisting
        # of the single digit x.
        # After processing a character, cnt[d][0] gives the number of substrings ending at this
        # position that are divisible by d. If the current digit is non‑zero, those substrings are
        # exactly the ones we need to add to the answer.
        # The algorithm runs in O(9 * sum_{d=1}^{9} d) = O(45) per character, well within limits.
        n = len(s)
        # Initialize remainder count tables for each divisor 1..9
        cnt = {d: [0] * d for d in range(1, 10)}  # cnt[d][r] = number of substrings ending at previous position with remainder r mod d
        ans = 0
        for ch in s:
            x = ord(ch) - ord('0')
            # Update tables for each divisor independently
            for d in range(1, 10):
                old = cnt[d]
                new = [0] * d
                # Substring consisting of just the current digit
                new[x % d] += 1
                # Extend all previous substrings ending at the previous position
                for r in range(d):
                    nr = (r * 10 + x) % d
                    new[nr] += old[r]
                cnt[d] = new
            # Add substrings where the last digit (x) is non‑zero and the substring is divisible by x
            if x != 0:
                ans += cnt[x][0]
        return ans
