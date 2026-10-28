import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    # 2-bit state: (a^b, b^c). Letter vectors:
    vec = {'A': 1, 'B': 3, 'C': 2}  # encode (x<<1)|y : A->(1,0)=2? fixed below
    # A: (a^b, b^c) flips: A -> (1,0); B -> (1,1); C -> (0,1)
    vec = {'A': 0b10, 'B': 0b11, 'C': 0b01}
    # state encoded as int 0..3 ; cnt tuple of length 4
    # DP: dict (cnt tuple, current state) -> ways
    init_cnt = [0, 0, 0, 0]
    init_cnt[0] = 1  # prefix of length 0 has state 0
    dp = {(tuple(init_cnt), 0): 1}
    for ch in s:
        letters = ['A', 'B', 'C'] if ch == '?' else [ch]
        ndp = {}
        for (cnt, cur), w in dp.items():
            for L in letters:
                ns = cur ^ vec[L]
                lst = list(cnt)
                lst[ns] += 1
                key = (tuple(lst), ns)
                ndp[key] = (ndp.get(key, 0) + w) % MOD
        dp = ndp
    ans = 0
    for (cnt, cur), w in dp.items():
        goods = sum(c * (c - 1) // 2 for c in cnt)
        if goods >= k:
            ans = (ans + w) % MOD
    print(ans)


main()
