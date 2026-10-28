import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]

    # Bit for each letter in the parity vector.
    bit = {'A': 1, 'B': 2, 'C': 4}
    # Class of a parity vector: {v, v^7} share the same class id (0..3).
    cls_of = [0] * 8
    cid = {}
    for v in range(8):
        key = min(v, v ^ 7)
        if key not in cid:
            cid[key] = len(cid)
        cls_of[v] = cid[key]
    # Weight 64 per class count (counts <= 51 < 64).
    shift = [1 << (6 * c) for c in range(4)]

    # State key: counts code * 8 + prefix parity vector v.
    # Initial prefix: parity vector 0, its class contributes one count.
    dp = {shift[cls_of[0]] * 8 + 0: 1}
    for ch in s:
        if ch == '?':
            letters = 'ABC'
        else:
            letters = ch
        ndp = {}
        get = ndp.get
        for key, ways in dp.items():
            code, v = divmod(key, 8)
            for L in letters:
                nv = v ^ bit[L]
                c = cls_of[nv]
                nkey = (code + shift[c]) * 8 + nv
                ndp[nkey] = (get(nkey, 0) + ways) % MOD
        dp = ndp

    total = 0
    for key, ways in dp.items():
        code = key // 8
        good = 0
        for c in range(4):
            m = (code >> (6 * c)) & 63
            good += m * (m - 1) // 2
        if good >= k:
            total = (total + ways) % MOD
    print(total)


main()
