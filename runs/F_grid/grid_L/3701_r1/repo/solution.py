class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n == 0:
            return ""
        if n < 3:
            return ""
        INF = float('inf')
        o = [ord(ch) - 97 for ch in caption]
        # F[i][c*4+k]: min cost for suffix i.., current run ends with letter c
        # with length k (k in 1..3, 3 means >=3), to finish validly.
        F = [None] * (n + 1)
        base = [INF] * 104
        for c in range(26):
            base[c * 4 + 3] = 0
        F[n] = base
        for i in range(n - 1, 0, -1):
            nxt = F[i + 1]
            # G[d] = cost of placing d at i starting a new run of length 1
            G = [abs(d - o[i]) + nxt[d * 4 + 1] for d in range(26)]
            # best two of G
            b1 = min(range(26), key=lambda d: G[d])
            v1 = G[b1]
            v2 = min((G[d] for d in range(26) if d != b1), default=INF)
            cur = [INF] * 104
            for c in range(26):
                cc = abs(c - o[i])
                cur[c * 4 + 1] = cc + nxt[c * 4 + 2]
                cur[c * 4 + 2] = cc + nxt[c * 4 + 3]
                alt = v1 if c != b1 else v2
                cur[c * 4 + 3] = min(cc + nxt[c * 4 + 3], alt)
            F[i] = cur
        # position 0: start new run with d
        best = INF
        bd = -1
        for d in range(26):
            v = abs(d - o[0]) + F[1][d * 4 + 1]
            if v < best:
                best = v
                bd = d
        if best == INF:
            return ""
        res = [chr(97 + bd)]
        c, k = bd, 1
        for i in range(1, n):
            V = F[i][c * 4 + k]
            nxt = F[i + 1]
            chosen = None
            for d in range(26):
                cd = abs(d - o[i])
                if d == c:
                    if k < 3:
                        if cd + nxt[c * 4 + k + 1] == V:
                            chosen = (d, k + 1)
                            break
                    else:
                        if cd + nxt[c * 4 + 3] == V:
                            chosen = (d, 3)
                            break
                else:
                    if k == 3 and cd + nxt[d * 4 + 1] == V:
                        chosen = (d, 1)
                        break
            d, k = chosen
            c = d
            res.append(chr(97 + d))
        return "".join(res)
