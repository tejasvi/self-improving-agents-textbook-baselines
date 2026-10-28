class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Edge case: k == 0 not possible per constraints (k >= 1)
        # Number of independent positions (left half including middle if odd)
        m = (n + 1) // 2
        # Precompute powers of 10 modulo k up to n-1
        pow10 = [1 % k]
        for i in range(1, n):
            pow10.append((pow10[-1] * 10) % k)
        # Compute weight for each independent position i (0-indexed from left)
        weights = []
        for i in range(m):
            j = n - 1 - i
            if i == j:  # middle position in odd length
                w = pow10[i] % k
            else:
                w = (pow10[i] + pow10[j]) % k
            weights.append(w)
        # suffix_possible[i] = list of booleans length k, indicating which remainders
        # can be achieved using positions i..m-1 (inclusive)
        suffix_possible = [[False] * k for _ in range(m + 1)]
        suffix_possible[m][0] = True  # no positions, remainder 0 achievable
        # Build DP backwards
        for i in range(m - 1, -1, -1):
            w = weights[i]
            for d in range(10):  # digit can be 0..9 (first digit constraint handled later)
                add = (d * w) % k
                for r_next in range(k):
                    if suffix_possible[i + 1][r_next]:
                        suffix_possible[i][(add + r_next) % k] = True
        # Now construct the largest palindrome greedily
        chosen = [0] * m
        cur_rem = 0  # remainder contributed by already fixed positions (0..i-1)
        for i in range(m):
            needed = (-cur_rem) % k  # we need (add + suffix) % k == needed
            w = weights[i]
            # Determine digit range: most significant cannot be zero
            start_digit = 9
            end_digit = 0
            if i == 0:
                digit_range = range(9, 0, -1)  # 9 down to 1
            else:
                digit_range = range(9, -1, -1)
            found = False
            for d in digit_range:
                add = (d * w) % k
                # we need a suffix remainder r_next such that (add + r_next) % k == needed
                for r_next in range(k):
                    if suffix_possible[i + 1][r_next] and (add + r_next) % k == needed:
                        chosen[i] = d
                        cur_rem = (cur_rem + add) % k
                        found = True
                        break
                if found:
                    break
            if not found:
                # No digit leads to a solution; return empty string (should not happen)
                return ""
        # Build full palindrome string
        left = ''.join(str(d) for d in chosen)
        if n % 2 == 0:
            right = left[::-1]
        else:
            right = left[-2::-1]  # exclude middle character
        return left + right
