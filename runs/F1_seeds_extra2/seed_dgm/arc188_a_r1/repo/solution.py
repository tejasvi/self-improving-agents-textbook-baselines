import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2] if len(data) > 2 else ""

    # Substring is good iff counts of A,B,C all have equal parity (non-empty).
    # Prefix parity vector P in {0,1}^3; group prefixes by the class {P, P^111}.
    # Class key = (P_A^P_B, P_B^P_C), i.e. 2 bits. Flipping A -> (1,0),
    # flipping B -> (1,1), flipping C -> (0,1).
    # Total good substrings = sum over classes of C(n_c, 2), where n_c is the
    # number of prefixes 0..N in class c.
    flips = {'A': 1, 'B': 3, 'C': 2}  # bit0 = x, bit1 = y ; A=(1,0)->1, B=(1,1)->3, C=(0,1)->2
    # state: (cur_class, n0, n1, n2, n3) -> count
    dp = {(0, 1, 0, 0, 0): 1}
    for i in range(n):
        ch = s[i]
        if ch == '?':
            opts = (1, 3, 2)
        else:
            opts = (flips[ch],)
        ndp = {}
        for key, val in dp.items():
            cur = key[0]
            cnt = list(key[1:])
            for f in opts:
                nc = cur ^ f
                cnt2 = cnt[:]
                cnt2[nc] += 1
                nk = (nc, cnt2[0], cnt2[1], cnt2[2], cnt2[3])
                ndp[nk] = (ndp.get(nk, 0) + val) % MOD
        dp = ndp

    ans = 0
    for key, val in dp.items():
        score = 0
        for c in key[1:]:
            score += c * (c - 1) // 2
        if score >= k:
            ans = (ans + val) % MOD
    print(ans % MOD)


main()
