import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = 101
    vals = list(map(int, data[1:1 + 6 * n]))
    cubs = []
    for i in range(n):
        b = 6 * i
        cubs.append((vals[b], vals[b + 1], vals[b + 2],
                     vals[b + 3], vals[b + 4], vals[b + 5]))
    ans = [0] * n
    # Lo[k][a]: flat grid over (p,q) of owner whose min along axis k == a
    # Hi[k][a]: owner whose max along axis k == a
    for k in range(3):
        p, q = (k + 1) % 3, (k + 2) % 3
        Lo = [[-1] * (S * S) for _ in range(S)]
        Hi = [[-1] * (S * S) for _ in range(S)]
        for i in range(n):
            c = cubs[i]
            lk, hk = c[k], c[k + 3]
            lp, hp = c[p], c[p + 3]
            lq, hq = c[q], c[q + 3]
            w = hq - lq
            ids = [i] * w
            gl = Lo[lk]
            gh = Hi[hk]
            for b in range(lp, hp):
                s = b * S + lq
                gl[s:s + w] = ids
                gh[s:s + w] = ids
        # query: cuboid i's high face at hk looks at Lo[hk]; low face at lk looks at Hi[lk]
        for i in range(n):
            c = cubs[i]
            lk, hk = c[k], c[k + 3]
            lp, hp = c[p], c[p + 3]
            lq, hq = c[q], c[q + 3]
            g1 = Lo[hk]
            g2 = Hi[lk]
            s1 = set()
            s2 = set()
            for b in range(lp, hp):
                s = b * S + lq
                e = b * S + hq
                s1.update(g1[s:e])
                s2.update(g2[s:e])
            s1.discard(-1)
            s2.discard(-1)
            s1.discard(i)
            s2.discard(i)
            ans[i] += len(s1) + len(s2)
    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
