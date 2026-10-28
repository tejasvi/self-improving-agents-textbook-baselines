import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    strs = data[1:1 + n]
    INF = float('inf')
    children = [{}]
    minlen = [INF]  # minimum length of any inserted string in subtree
    out = []
    for s in strs:
        m = len(s)
        # For previous S_j with lcp L with s, cost = m + |S_j| - 2L (or m, by emptying).
        best = minlen[0]
        node = 0
        d = 0
        for c in s:
            nxt = children[node].get(c)
            if nxt is None:
                break
            node = nxt
            d += 1
            v = minlen[node] - 2 * d
            if v < best:
                best = v
        ans = m
        if best < INF:
            ans = min(ans, m + best)
        out.append(ans)
        # insert s
        if m < minlen[0]:
            minlen[0] = m
        node = 0
        for c in s:
            nxt = children[node].get(c)
            if nxt is None:
                nxt = len(children)
                children.append({})
                minlen.append(INF)
                children[node][c] = nxt
            node = nxt
            if m < minlen[node]:
                minlen[node] = m
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
