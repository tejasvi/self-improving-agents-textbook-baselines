class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Edge case: k == 0 not possible per constraints (k >= 1)
        # If k == 1, any palindrome works, so the largest is all 9s.
        if k == 1:
            return "9" * n
        # Precompute powers of 10 modulo k up to n-1
        pow10_mod = [0] * n
        cur = 1 % k
        for i in range(n):
            pow10_mod[i] = cur
            cur = (cur * 10) % k
        # Number of independent positions (first half, including middle if odd)
        m = (n + 1) // 2
        # For each independent position, compute the coefficient (mod k) that multiplies the digit
        coeff = [0] * m
        for i in range(m):
            j = n - 1 - i
            if i == j:  # middle position in odd length
                coeff[i] = pow10_mod[i] % k
            else:
                coeff[i] = (pow10_mod[i] + pow10_mod[j]) % k
        # dp_masks[pos] -> bitmask of reachable remainders for suffix starting at pos
        # dp_masks[m] corresponds to empty suffix -> only remainder 0 reachable
        dp_masks = [0] * (m + 1)
        dp_masks[m] = 1 << 0
        # Build DP backwards
        for pos in range(m - 1, -1, -1):
            mask = 0
            start_digit = 1 if pos == 0 else 0
            for d in range(start_digit, 10):
                contrib = (d * coeff[pos]) % k
                # combine with all remainders reachable from suffix
                suffix_mask = dp_masks[pos + 1]
                # iterate over possible remainders in suffix_mask
                r = 0
                while suffix_mask:
                    # get lowest set bit index
                    if suffix_mask & 1:
                        new_rem = (contrib + r) % k
                        mask |= 1 << new_rem
                    suffix_mask >>= 1
                    r += 1
            dp_masks[pos] = mask
        # If remainder 0 is not reachable from the start, no solution
        if not (dp_masks[0] >> 0 & 1):
            return ""
        # Greedy construction of the largest palindrome
        chosen = [0] * m
        current_sum = 0  # sum of contributions of already chosen digits modulo k
        for pos in range(m):
            start_digit = 1 if pos == 0 else 0
            for d in range(9, start_digit - 1, -1):
                contrib = (d * coeff[pos]) % k
                new_sum = (current_sum + contrib) % k
                needed_suffix = (k - new_sum) % k
                if dp_masks[pos + 1] >> needed_suffix & 1:
                    chosen[pos] = d
                    current_sum = new_sum
                    break
        # Build the full palindrome string
        res = []
        for i in range(n):
            if i < m:
                res.append(str(chosen[i]))
            else:
                res.append(str(chosen[n - 1 - i]))
        return "".join(res)
