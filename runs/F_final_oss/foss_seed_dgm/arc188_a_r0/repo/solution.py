# Solution for ABC Symmetry problem
# Counts substrings where counts of A,B,C have same parity.
# Uses DP over prefix parity states (4 possible) and counts of occurrences.

import sys
MOD = 998244353

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    S = data[2]
    # State encoding: bits (x, y) where
    # x = parity(A) xor parity(B)
    # y = parity(A) xor parity(C)
    # There are 4 states: 0..3
    # Transition table: trans[state][char] -> new_state
    # char: 0=A, 1=B, 2=C
    trans = [[0]*3 for _ in range(4)]
    for s in range(4):
        x = (s >> 1) & 1
        y = s & 1
        # add A: toggle both bits
        ns = ((x ^ 1) << 1) | (y ^ 1)
        trans[s][0] = ns
        # add B: toggle x only
        ns = ((x ^ 1) << 1) | y
        trans[s][1] = ns
        # add C: toggle y only
        ns = (x << 1) | (y ^ 1)
        trans[s][2] = ns

    from collections import defaultdict
    # dp maps (c0,c1,c2,c3, cur_state) -> number of ways (mod MOD)
    # initial empty prefix: one occurrence of state 0
    dp = defaultdict(int)
    dp[(1, 0, 0, 0, 0)] = 1

    for ch in S:
        ndp = defaultdict(int)
        if ch == '?':
            letters = [0, 1, 2]
        elif ch == 'A':
            letters = [0]
        elif ch == 'B':
            letters = [1]
        else:  # 'C'
            letters = [2]
        for (c0, c1, c2, c3, cur_state), ways in dp.items():
            cnts = [c0, c1, c2, c3]
            for L in letters:
                ns = trans[cur_state][L]
                ncnts = cnts.copy()
                ncnts[ns] += 1
                key = (ncnts[0], ncnts[1], ncnts[2], ncnts[3], ns)
                ndp[key] = (ndp[key] + ways) % MOD
        dp = ndp

    ans = 0
    for (c0, c1, c2, c3, _), ways in dp.items():
        total = (c0 * (c0 - 1) // 2 +
                 c1 * (c1 - 1) // 2 +
                 c2 * (c2 - 1) // 2 +
                 c3 * (c3 - 1) // 2)
        if total >= K:
            ans = (ans + ways) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
