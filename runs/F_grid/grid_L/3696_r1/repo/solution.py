class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # S[k]: prefix digit sum (divisibility by 3 and 9).
        # W[k]: prefix value mod 7 times 5^k (10 * 5 = 1 mod 7), so that
        # substring s[i..j] is divisible by 7 iff W[i] == W[j+1].
        S = [0] * (n + 1)
        W = [0] * (n + 1)
        V = 0
        p = 1
        for k in range(n):
            d = ord(s[k]) - 48
            S[k + 1] = S[k] + d
            V = (V * 10 + d) % 7
            p = p * 5 % 7
            W[k + 1] = V * p % 7

        cnt3 = [0] * 3
        cnt9 = [0] * 9
        cnt7 = [0] * 7
        cnt3[0] += 1
        cnt9[0] += 1
        cnt7[0] += 1  # W[0] = 0

        total = 0
        for j in range(n):
            d = ord(s[j]) - 48
            if d != 0:
                if d == 1:
                    total += j + 1
                elif d in (2, 4, 5, 8):
                    k = {2: 1, 5: 1, 4: 2, 8: 3}[d]
                    # Substrings shorter than k: check directly.
                    for i in range(j, max(j - k + 1, -1), -1):
                        if int(s[i:j + 1]) % d == 0:
                            total += 1
                    # Substrings of length >= k: decided by last k digits.
                    if j - k + 1 >= 0 and int(s[j - k + 1:j + 1]) % d == 0:
                        total += j - k + 2
                elif d in (3, 6):
                    # 6 is even, so only divisibility by 3 matters.
                    total += cnt3[S[j + 1] % 3]
                elif d == 9:
                    total += cnt9[S[j + 1] % 9]
                elif d == 7:
                    total += cnt7[W[j + 1]]
            cnt3[S[j + 1] % 3] += 1
            cnt9[S[j + 1] % 9] += 1
            cnt7[W[j + 1]] += 1
        return total
