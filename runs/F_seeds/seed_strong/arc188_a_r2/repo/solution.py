import sys
from collections import defaultdict

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    bit = {'A': 1, 'B': 2, 'C': 4}
    # Prefix parity state (3 bits). Substring i..j is good iff its parity
    # vector is 000 or 111, i.e. prefix states lie in the same class {x, x^7}.
    # Class of state x = min(x, x^7). Each class holds one state of each
    # weight-parity, and weight parity equals prefix length parity, so the
    # exact state is determined by class and length; we still track it exactly.
    start_cnt = (1, 0, 0, 0)
    dp = {(start_cnt, 0): 1}
    for ch in s:
        if ch == '?':
            letters = (1, 2, 4)
        else:
            letters = (bit[ch],)
        ndp = defaultdict(int)
        for (cnt, st), v in dp.items():
            for e in letters:
                ns = st ^ e
                c = min(ns, ns ^ 7)
                nc = list(cnt)
                nc[c] += 1
                ndp[(tuple(nc), ns)] += v
        dp = {key: val % MOD for key, val in ndp.items()}
    ans = 0
    for (cnt, st), v in dp.items():
        good = 0
        for x in cnt:
            good += x * (x - 1) // 2
        if good >= k:
            ans += v
    print(ans % MOD)


main()
