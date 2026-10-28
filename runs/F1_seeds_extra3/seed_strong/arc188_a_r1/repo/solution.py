import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); K = int(data[1]); S = data[2]
    MOD = 998244353

    # parity vector bits: A=1, B=2, C=4. Good substring <=> prefix parity vectors
    # equal or complementary (v ^ 7). Classes = canon(v) = min(v, v^7).
    def canon(v):
        return min(v, v ^ 7)
    reps = sorted(set(canon(v) for v in range(8)))  # 4 classes
    cidx = {r: i for i, r in enumerate(reps)}
    cls_of = [cidx[canon(v)] for v in range(8)]
    # transition: class k, letter bit e -> class
    trans = [[0] * 3 for _ in range(4)]
    for k, r in enumerate(reps):
        for x, e in enumerate((1, 2, 4)):
            trans[k][x] = cls_of[r ^ e]

    # state key: counts packed base 64 in 4 digits (bits 0..23 digits 0..3 each 6 bits),
    # plus current class in low 2 bits.
    W = [1 << (6 * k + 2) for k in range(4)]
    init = {W[cls_of[0]] | cls_of[0]: 1}
    cur = init
    for i in range(N):
        ch = S[i]
        if ch == '?':
            opts = [0, 1, 2]
        else:
            opts = [{'A': 0, 'B': 1, 'C': 2}[ch]]
        nd = {}
        get = nd.get
        for key, val in cur.items():
            c = key & 3
            base = key & ~3
            for x in opts:
                nc = trans[c][x]
                nk = base + W[nc] + nc
                nd[nk] = (get(nk, 0) + val) % MOD
        cur = nd
    ans = 0
    for key, val in cur.items():
        F = 0
        for k in range(4):
            n = (key >> (6 * k + 2)) & 63
            F += n * (n - 1) // 2
        if F >= K:
            ans += val
    print(ans % MOD)

main()
