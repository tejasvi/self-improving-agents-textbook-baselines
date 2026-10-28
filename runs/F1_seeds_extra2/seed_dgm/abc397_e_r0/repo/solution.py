import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); K = int(data[1])
    M = N * K
    if K == 1:
        print("Yes")
        return
    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    # BFS order from root 1
    parent = [0] * (M + 1)
    visited = [False] * (M + 1)
    order = [1]
    visited[1] = True
    for v in order:
        for w in adj[v]:
            if not visited[w]:
                visited[w] = True
                parent[w] = v
                order.append(w)
    # opens[v]: list of open chain lengths from children
    opens_cnt = [0] * (M + 1)
    opens_sum = [0] * (M + 1)
    res = [0] * (M + 1)
    for v in reversed(order):
        c = opens_cnt[v]
        if c == 0:
            r = 1
        elif c == 1:
            r = opens_sum[v] + 1
            if r == K:
                r = 0
        elif c == 2:
            r = opens_sum[v] + 1
            if r != K:
                print("No")
                return
            r = 0
        else:
            print("No")
            return
        res[v] = r
        p = parent[v]
        if p and r > 0:
            opens_cnt[p] += 1
            opens_sum[p] += r
    if res[1] != 0:
        print("No")
    else:
        print("Yes")

main()
