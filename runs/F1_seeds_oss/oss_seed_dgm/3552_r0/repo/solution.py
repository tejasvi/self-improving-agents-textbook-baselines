class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Edge case: k == 0 not possible as per constraints (k >= 1)
        # Number of independent positions (first half, including middle if n odd)
        m = (n + 1) // 2
        # Precompute 10^i mod k for i = 0..n-1
        pow10_mod = [1 % k]
        for i in range(1, n):
            pow10_mod.append((pow10_mod[-1] * 10) % k)
        # Coefficients for each independent position
        coeff = [0] * m
        for pos in range(m):
            left_pow = pow10_mod[n - 1 - pos]
            right_pow = pow10_mod[pos]
            if n - 1 - pos != pos:  # not the middle digit of odd length
                coeff[pos] = (left_pow + right_pow) % k
            else:
                coeff[pos] = right_pow % k
        # DP suffix reachable remainders
        # reachable[pos][r] == True if we can reach remainder r using positions pos..m-1
        reachable = [[False] * k for _ in range(m + 1)]
        reachable[m][0] = True  # no positions left -> remainder 0 achievable
        for pos in range(m - 1, -1, -1):
            for r_next in range(k):
                if not reachable[pos + 1][r_next]:
                    continue
                # Try all digits 0..9 (later we will enforce leading non-zero when constructing)
                for d in range(10):
                    new_r = (d * coeff[pos] + r_next) % k
                    reachable[pos][new_r] = True
        # Greedy construction of the largest palindrome
        digits = [0] * m
        current_rem = 0
        for pos in range(m):
            chosen = -1
            # Digits to try: 9 down to 0 (but pos==0 cannot be 0)
            for d in range(9, -1, -1):
                if pos == 0 and d == 0:
                    continue
                new_rem = (current_rem + d * coeff[pos]) % k
                needed = (k - new_rem) % k
                if reachable[pos + 1][needed]:
                    chosen = d
                    current_rem = new_rem
                    break
            if chosen == -1:
                # No possible digit, return empty string (no solution)
                return ""
            digits[pos] = chosen
        # At this point current_rem should be such that we can finish with remainder 0
        # Verify (optional)
        if current_rem % k != 0:
            # In case of unexpected failure
            return ""
        # Build the full palindrome string
        chars = []
        for i in range(n):
            if i < m:
                chars.append(str(digits[i]))
            else:
                chars.append(str(digits[n - 1 - i]))
        return "".join(chars)
