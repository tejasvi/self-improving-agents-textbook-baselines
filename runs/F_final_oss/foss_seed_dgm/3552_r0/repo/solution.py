class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Handle trivial case where any palindrome works (k == 1)
        if k == 1:
            return '9' * n

        # Precompute 10^i mod k for i = 0 .. n-1
        pow10_mod = [0] * n
        pow10_mod[0] = 1 % k
        for i in range(1, n):
            pow10_mod[i] = (pow10_mod[i - 1] * 10) % k

        L = (n + 1) // 2  # number of independent positions (first half)
        weights = [0] * L
        for i in range(L):
            if n % 2 == 1 and i == L - 1:  # middle digit for odd length
                weights[i] = pow10_mod[i] % k
            else:
                weights[i] = (pow10_mod[n - 1 - i] + pow10_mod[i]) % k

        # suffix_possible[pos] = set of remainders achievable from pos .. L-1
        suffix_possible = [set() for _ in range(L + 1)]
        suffix_possible[L].add(0)
        for pos in range(L - 1, -1, -1):
            cur_set = set()
            w = weights[pos]
            for d in range(10):
                for r in suffix_possible[pos + 1]:
                    cur_set.add((d * w + r) % k)
            suffix_possible[pos] = cur_set

        # Build the largest palindrome digit by digit
        digits = []
        cur_mod = 0  # sum of contributions of already chosen digits modulo k
        for pos in range(L):
            w = weights[pos]
            found = False
            for d in range(9, -1, -1):
                if pos == 0 and d == 0:
                    continue  # leading zero not allowed
                new_mod = (cur_mod + d * w) % k
                need = (-new_mod) % k
                if need in suffix_possible[pos + 1]:
                    digits.append(str(d))
                    cur_mod = new_mod
                    found = True
                    break
            if not found:
                # Should never happen according to problem guarantees
                return ""

        # Construct full palindrome string
        first_half = ''.join(digits)
        if n % 2 == 0:
            palindrome = first_half + first_half[::-1]
        else:
            if L == 1:
                palindrome = first_half  # single digit case
            else:
                palindrome = first_half + first_half[-2::-1]
        return palindrome
