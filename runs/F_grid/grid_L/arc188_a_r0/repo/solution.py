import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    S = data[2]

    # A substring is good iff the counts of A, B, C all have the same parity.
    # Encode prefix parity pattern by state = 2*(pa^pb) + (pb^pc).
    # Two prefixes bound a good substring iff their states are equal.
    # Letter effects on state: A -> 2, B -> 3, C -> 1.
    eff = {'A': 2, 'B': 3, 'C': 1}

    # dp key: (state, cnt0, cnt1, cnt2, cnt3)
    dp = {(0, 1, 0, 0, 0): 1}
    for pos in range(N):
        ch = S[pos]
        opts = ['A', 'B', 'C'] if ch == '?' else [ch]
        ndp = {}
        for key, w in dp.items():
            st = key[0]
            for c in opts:
                ns = st ^ eff[c]
                nk = list(key)
                nk[0] = ns
                nk[1 + ns] += 1
                nk = tuple(nk)
                ndp[nk] = (ndp.get(nk, 0) + w) % MOD
        dp = ndp

    ans = 0
    for key, w in dp.items():
        good = 0
        for c in key[1:]:
            good += c * (c - 1) // 2
        if good >= K:
            ans = (ans + w) % MOD
    print(ans)


main()
