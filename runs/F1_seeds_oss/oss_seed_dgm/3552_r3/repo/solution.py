class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Edge case: k == 1, any palindrome works, return the largest n-digit palindrome (all 9s)
        if k == 1:
            return '9' * n

        # Precompute powers of 10 modulo k
        # pow10[e] = 10^e % k for e from 0 to n-1
        pow10 = [1 % k]
        for _ in range(1, n):
            pow10.append((pow10[-1] * 10) % k)

        # Number of positions we need to decide (left half including middle if n is odd)
        left_end = (n - 1) // 2  # inclusive index of the last position to set

        # Coefficients for each position in the left half (including middle)
        coeff = [0] * (left_end + 1)
        for i in range(left_end + 1):
            j = n - 1 - i
            if i != j:
                # contribution from position i and its mirror j
                coeff[i] = (pow10[n - 1 - i] + pow10[i]) % k
            else:
                # middle position in odd length
                coeff[i] = pow10[i] % k

        # DP from the rightmost position of the left half to compute reachable residues
        # mask[pos] is a bitmask where bit r is set if residue r (mod k) can be achieved
        # using positions pos..left_end.
        mask = [0] * (left_end + 2)  # extra slot for the base case after the last position
        mask[left_end + 1] = 1 << 0  # only residue 0 is achievable with no digits left

        for pos in range(left_end, -1, -1):
            cur_mask = 0
            c = coeff[pos]
            for r in range(k):
                if (mask[pos + 1] >> r) & 1:
                    # Try all allowed digits for this position
                    for d in range(10):
                        if pos == 0 and d == 0:
                            continue  # leading zero not allowed
                        new_res = (d * c + r) % k
                        cur_mask |= 1 << new_res
            mask[pos] = cur_mask

        # Greedy construction of the largest palindrome
        current_mod = 0
        left_digits = []  # digits for positions 0..left_end as strings
        for i in range(left_end + 1):
            chosen = None
            for d in range(9, -1, -1):
                if i == 0 and d == 0:
                    continue
                new_mod = (current_mod + d * coeff[i]) % k
                needed = (-new_mod) % k
                if (mask[i + 1] >> needed) & 1:
                    chosen = d
                    current_mod = new_mod
                    left_digits.append(str(d))
                    break
            if chosen is None:
                # No valid digit found – this should not happen under problem constraints
                return ""

        # Build the full palindrome string
        if n % 2 == 0:
            # even length: mirror the whole left part
            right = ''.join(reversed(left_digits))
            return ''.join(left_digits) + right
        else:
            # odd length: the last digit of left_digits is the middle digit
            middle = left_digits[-1]
            left_part = left_digits[:-1]
            right = ''.join(reversed(left_part))
            return ''.join(left_part) + middle + right
