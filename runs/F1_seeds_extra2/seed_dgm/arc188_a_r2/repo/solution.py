import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s_str = data[2] if len(data) > 2 else ""
    bits = {'A': 1, 'B': 2, 'C': 4}
    # parity-state class: s and s^7 share a class; class id = min(s, s^7) mapped to 0..3
    cls_of = [0] * 8
    cls_id = {}
    for s in range(8):
        m = min(s, s ^ 7)
        if m not in cls_id:
            cls_id[m] = len(cls_id)
        cls_of[s] = cls_id[m]

    # DP: key = (parity state s, cnt tuple over 4 classes)
    start_cnt = [0, 0, 0, 0]
    start_cnt[cls_of[0]] = 1
    dp = {(0, tuple(start_cnt)): 1}
    for i in range(n):
        ch = s_str[i]
        if ch == '?':
            letters = [1, 2, 4]
        else:
            letters = [bits[ch]]
        ndp = {}
        for (s, cnt), v in dp.items():
            for b in letters:
                ns = s ^ b
                c = cls_of[ns]
                nc = list(cnt)
                nc[c] += 1
                key = (ns, tuple(nc))
                ndp[key] = (ndp.get(key, 0) + v) % MOD
        dp = ndp

    total = 0
    for (s, cnt), v in dp.items():
        good = sum(c * (c - 1) // 2 for c in cnt)
        if good >= k:
            total = (total + v) % MOD
    print(total % MOD)


main()
