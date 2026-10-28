import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    V = 26
    edges = []
    for s in names:
        edges.append((ord(s[0]) - 65, ord(s[1]) - 65))
    m = len(edges)

    # reachability on letters (reflexive)
    reach = [[i == j for j in range(V)] for i in range(V)]
    for (u, v) in edges:
        reach[u][v] = True
    for k in range(V):
        rk = reach[k]
        for i in range(V):
            if reach[i][k]:
                ri = reach[i]
                for j in range(V):
                    if rk[j]:
                        ri[j] = True

    # preorder on edges: e1 <= e2 iff head(e1) reaches tail(e2)
    le = [[reach[edges[a][1]][edges[b][0]] for b in range(m)] for a in range(m)]

    # group mutually comparable edges into classes
    cls = [-1] * m
    reps = []
    for a in range(m):
        if cls[a] != -1:
            continue
        c = len(reps)
        reps.append(a)
        for b in range(m):
            if cls[b] == -1 and le[a][b] and le[b][a]:
                cls[b] = c
    k = len(reps)

    # strict order between classes
    adj = [[] for _ in range(k)]
    for i in range(k):
        ri = reps[i]
        for j in range(k):
            if i != j and le[ri][reps[j]]:
                adj[i].append(j)

    # maximum bipartite matching (Kuhn's algorithm)
    match_r = [-1] * k
    sys.setrecursionlimit(10000)

    def try_kuhn(u, seen):
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True
                if match_r[w] == -1 or try_kuhn(match_r[w], seen):
                    match_r[w] = u
                    return True
        return False

    matching = 0
    for u in range(k):
        if try_kuhn(u, [False] * k):
            matching += 1

    print(k - matching)


main()
