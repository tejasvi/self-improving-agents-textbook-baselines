import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    V = 26
    out_deg = [0] * V
    in_deg = [0] * V
    reach = [[False] * V for _ in range(V)]
    parent = list(range(V))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    used = [False] * V
    for s in names:
        a = ord(s[0]) - 65
        b = ord(s[1]) - 65
        out_deg[a] += 1
        in_deg[b] += 1
        reach[a][b] = True
        used[a] = used[b] = True
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    # transitive closure (paths of length >= 1)
    for k in range(V):
        rk = reach[k]
        for i in range(V):
            if reach[i][k]:
                ri = reach[i]
                for j in range(V):
                    if rk[j]:
                        ri[j] = True

    imb = [out_deg[v] - in_deg[v] for v in range(V)]
    comps = {}
    for v in range(V):
        if used[v]:
            comps.setdefault(find(v), []).append(v)

    total = 0
    for members in comps.values():
        surplus = [v for v in members if imb[v] > 0]
        deficit = [v for v in members if imb[v] < 0]
        P = sum(imb[v] for v in surplus)
        if P == 0:
            total += 1
            continue
        # Units: each deficit unit b may match a surplus unit a if b reaches a.
        left_units = []  # deficit units
        for b in deficit:
            left_units.extend([b] * (-imb[b]))
        right_units = []  # surplus units
        for a in surplus:
            right_units.extend([a] * imb[a])
        adj = []
        for b in left_units:
            adj.append([j for j, a in enumerate(right_units) if reach[b][a]])
        match_r = [-1] * len(right_units)

        def try_kuhn(u, seen):
            for j in adj[u]:
                if not seen[j]:
                    seen[j] = True
                    if match_r[j] == -1 or try_kuhn(match_r[j], seen):
                        match_r[j] = u
                        return True
            return False

        M = 0
        for u in range(len(left_units)):
            seen = [False] * len(right_units)
            if try_kuhn(u, seen):
                M += 1
        total += max(1, P - M)
    print(total)


main()
