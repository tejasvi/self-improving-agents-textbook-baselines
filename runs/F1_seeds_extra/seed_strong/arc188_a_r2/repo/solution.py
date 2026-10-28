import sys
from math import comb

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); k = int(data[1]); s = data[2]
    # Prefix parity class: (x^y, y^z) in Z2^2; A flips bit0, B flips both, C flips bit1.
    flip = {'A': 1, 'B': 3, 'C': 2}
    # state key: (cls << 24) | packed histogram (6 bits per class count)
    dp = {(0 << 24) | (1 << 0): 1}  # cls=0, m0=1
    for ch in s:
        opts = [flip[ch]] if ch in flip else [1, 3, 2]
        ndp = {}
        get = ndp.get
        for key, val in dp.items():
            cls = key >> 24
            packed = key & ((1 << 24) - 1)
            for d in opts:
                nc = cls ^ d
                nk = (nc << 24) | (packed + (1 << (6 * nc)))
                ndp[nk] = (get(nk, 0) + val) % MOD
        dp = ndp
    ans = 0
    for key, val in dp.items():
        packed = key & ((1 << 24) - 1)
        score = 0
        for g in range(4):
            m = (packed >> (6 * g)) & 63
            score += m * (m - 1) // 2
        if score >= k:
            ans = (ans + val) % MOD
    print(ans)

main()
