from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # moduli coprime to 10 for hashing approach
        mods = (3, 7, 9)
        inv = {m: pow(10, -1, m) for m in mods}
        # Q-values for prefix index i: P[i] * inv10^i mod m
        cnt = {m: [0] * m for m in mods}
        q = {m: 0 for m in mods}  # current Q[e] for each modulus
        # Q[0] = 0 for all moduli; insert it
        for m in mods:
            cnt[m][0] += 1
        # for 2,4,8 handling: track value of last digits
        total = 0
        for e in range(1, n + 1):
            c = s[e - 1]
            d = ord(c) - 48
            # update Q[e] = (P[e]) * inv^e ; P[e] = 10*P[e-1]+d
            # Q[e] = (P[e-1]*10 + d) * inv^e = Q[e-1]*10*inv + d*inv^e
            # Easier: maintain pw[m] = inv^e, P[m] = P[e] mod m
            if e == 1:
                pw = {m: 1 for m in mods}
                pv = {m: 0 for m in mods}
            # update
            for m in mods:
                pv[m] = (pv[m] * 10 + d) % m
                pw[m] = pw[m] * inv[m] % m
                q[m] = pv[m] * pw[m] % m
            if d == 0:
                for m in mods:
                    cnt[m][q[m]] += 1
                continue
            if d == 1 or d == 5:
                total += e
            elif d == 2 or d == 4 or d == 8:
                # substrings ending at e-1 (index j = e-1), length L
                # length 1: always divisible
                total += 1
                # length 2
                if e >= 2:
                    v2 = int(s[e - 2:e])
                    if v2 % d == 0:
                        total += 1
                # length >= 3: last 3 digits value mod 8 (and 1000 ≡ 0 mod 8)
                if e >= 3:
                    v3 = int(s[e - 3:e])
                    if v3 % d == 0:
                        total += e - 2  # i from 0..e-3 inclusive
            elif d == 3 or d == 6:
                total += cnt[3][q[3]]
            elif d == 7:
                total += cnt[7][q[7]]
            elif d == 9:
                total += cnt[9][q[9]]
            # insert Q[e] for future queries
            for m in mods:
                cnt[m][q[m]] += 1
        return total
