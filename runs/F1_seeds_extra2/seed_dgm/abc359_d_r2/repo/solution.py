import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    K = int(data[1])
    S = data[2]
    MOD = 998244353

    # pal[x]: whether the K-bit number x reads the same reversed
    pal = [False] * (1 << K)
    for x in range(1 << K):
        r = 0
        y = x
        for _ in range(K):
            r = (r << 1) | (y & 1)
            y >>= 1
        pal[x] = (r == x)

    K1 = K - 1
    maskK1 = (1 << K1) - 1

    dp = [1]  # masks of length i (i < K-1)
    for i in range(N):
        c = S[i]
        opts = (0, 1) if c == '?' else ((0,) if c == 'A' else (1,))
        if i < K1:
            nd = [0] * (1 << (i + 1))
            for m, v in enumerate(dp):
                if v:
                    for b in opts:
                        nm = (m << 1) | b
                        nd[nm] = (nd[nm] + v) % MOD
            dp = nd
        else:
            nd = [0] * (1 << K1)
            for m, v in enumerate(dp):
                if v:
                    for b in opts:
                        full = (m << 1) | b
                        if not pal[full]:
                            nm = full & maskK1
                            nd[nm] = (nd[nm] + v) % MOD
            dp = nd

    print(sum(dp) % MOD)

main()
