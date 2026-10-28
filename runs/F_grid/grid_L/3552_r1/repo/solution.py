class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # pw[e] = 10^e mod k
        pw = [1 % k] * n
        for e in range(1, n):
            pw[e] = pw[e - 1] * 10 % k
        # weight of half-digit at position i
        w = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w.append(pw[i])
            else:
                w.append((pw[i] + pw[j]) % k)
        # reach[i][t]: positions i..h-1 can be filled so that their sum = t (mod k)
        reach = [None] * (h + 1)
        reach[h] = [False] * k
        reach[h][0] = True
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            cur = [False] * k
            nxt = reach[i + 1]
            wi = w[i]
            for t in range(k):
                for d in range(lo, 10):
                    if nxt[(t - d * wi) % k]:
                        cur[t] = True
                        break
            reach[i] = cur
        if not reach[0][0]:
            return ""
        res = []
        t = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            wi = w[i]
            nxt = reach[i + 1]
            for d in range(9, lo - 1, -1):
                nt = (t - d * wi) % k
                if nxt[nt]:
                    res.append(d)
                    t = nt
                    break
        s = [str(d) for d in res]
        full = s + s[: n // 2][::-1]
        return "".join(full)
