class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # weight[i]: contribution mod k of digit at position i (and its mirror)
        weight = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                weight.append(pow(10, i, k))
            else:
                weight.append((pow(10, i, k) + pow(10, j, k)) % k)

        def allowed(i):
            return range(1, 10) if i == 0 else range(0, 10)

        # reach[i][r]: residue r is achievable as sum of contributions of positions i..h-1
        reach = [None] * (h + 1)
        base = [False] * k
        base[0] = True
        reach[h] = base
        for i in range(h - 1, -1, -1):
            w = weight[i]
            vals = {(d * w) % k for d in allowed(i)}
            nxt = reach[i + 1]
            cur = [False] * k
            for r in range(k):
                if nxt[r]:
                    for v in vals:
                        cur[(r + v) % k] = True
            reach[i] = cur

        if not reach[0][0]:
            return ""

        digits = [0] * h
        acc = 0
        for i in range(h):
            w = weight[i]
            nxt = reach[i + 1]
            for d in range(9, -1, -1):
                if i == 0 and d == 0:
                    continue
                c = (acc + d * w) % k
                if nxt[(-c) % k]:
                    digits[i] = d
                    acc = c
                    break

        res = [0] * n
        for i in range(h):
            res[i] = digits[i]
            res[n - 1 - i] = digits[i]
        return "".join(map(str, res))
