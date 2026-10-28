import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    total = n * k
    if total == 1:
        print("Yes")
        return
    adj = [[] for _ in range(total + 1)]
    idx = 2
    for _ in range(total - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    parent = [0] * (total + 1)
    order = [1]
    visited = [False] * (total + 1)
    visited[1] = True
    i = 0
    while i < len(order):
        x = order[i]
        i += 1
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                order.append(y)

    # cnt[v]: number of open child chains (length < K) attached to v
    # sm[v]: sum of those open chain lengths
    cnt = [0] * (total + 1)
    sm = [0] * (total + 1)

    for v in reversed(order):
        c = cnt[v]
        if c > 2:
            print("No")
            return
        p = 1 + sm[v]
        if p > k:
            print("No")
            return
        if c == 2 or p == k:
            # path closes at v: must be exactly K
            if p != k:
                print("No")
                return
            closed = True
        else:
            closed = False
        par = parent[v]
        if par == 0:
            # root: must be closed
            if not closed:
                print("No")
                return
        elif not closed:
            cnt[par] += 1
            sm[par] += p
    print("Yes")


main()
