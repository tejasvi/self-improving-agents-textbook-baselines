class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        INF = float("inf")
        s = [ord(ch) - 97 for ch in caption]
        # f[i][c*3 + (r-1)]: min cost to finish suffix i, given previous char c
        # and current run length r (r capped at 3; r==3 means run is complete).
        f = [None] * (n + 1)
        f[n] = [INF] * 78
        for c in range(26):
            f[n][c * 3 + 2] = 0  # r == 3
        for i in range(n - 1, -1, -1):
            f1 = f[i + 1]
            si = s[i]
            # h[d] = cost to place d at i and start a new run of d
            h = [abs(si - d) + f1[d * 3] for d in range(26)]
            # best two distinct-char minima of h
            b1 = b2 = INF
            a1 = -1
            for d in range(26):
                v = h[d]
                if v < b1:
                    b2 = b1
                    b1 = v
                    a1 = d
                elif v < b2:
                    b2 = v
            cur = [INF] * 78
            for c in range(26):
                cost_c = abs(si - c)
                base = c * 3
                # r = 1 and r = 2: must continue same char
                cur[base] = cost_c + f1[base + 1]
                cur[base + 1] = cost_c + f1[base + 2]
                # r = 3: may continue same char or switch to new char
                m = b2 if a1 == c else b1
                cur[base + 2] = min(cost_c + f1[base + 2], m)
            f[i] = cur
        # start: no previous char; first run starts with any d
        start_best = INF
        for d in range(26):
            v = abs(s[0] - d) + f[1][d * 3]
            if v < start_best:
                start_best = v
        if start_best >= INF:
            return ""
        # Reconstruct lexicographically smallest optimal string
        res = []
        c, r = -1, 3
        for i in range(n):
            target = start_best if i == 0 else f[i][c * 3 + r - 1]
            si = s[i]
            fn = f[i + 1]
            chosen = False
            for d in range(26):
                if d == c:
                    if r == 3:
                        nc, nr = c, 3
                    else:
                        nc, nr = c, r + 1
                elif r == 3 or c == -1:
                    nc, nr = d, 1
                else:
                    continue
                if abs(si - d) + fn[nc * 3 + nr - 1] == target:
                    res.append(chr(97 + d))
                    c, r = nc, nr
                    chosen = True
                    break
            if not chosen:
                return ""
        return "".join(res)
