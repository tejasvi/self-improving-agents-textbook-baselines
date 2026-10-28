import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]
    indeg = [0] * n
    for x in a:
        indeg[x] += 1
    # Kahn peeling: vertices removed are tail (non-cycle) vertices.
    q = [i for i in range(n) if indeg[i] == 0]
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
    on_cycle = [indeg[i] > 0 for i in range(n)]
    # Cycle length for each cycle vertex.
    L = [0] * n
    seen = [False] * n
    for i in range(n):
        if on_cycle[i] and not seen[i]:
            members = []
            j = i
            while not seen[j]:
                seen[j] = True
                members.append(j)
                j = a[j]
            for m in members:
                L[m] = len(members)
    # Process tail vertices in reverse peel order: parents before children.
    t = [0] * n  # number of tail vertices on path from u (incl. u) to cycle
    for u in reversed(q):
        if not on_cycle[u]:
            t[u] = t[a[u]] + 1
            L[u] = L[a[u]]
    ans = 0
    for i in range(n):
        ans += t[i] + L[i]
    print(ans)

main()
