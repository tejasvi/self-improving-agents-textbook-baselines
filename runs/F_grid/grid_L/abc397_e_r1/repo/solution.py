import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); K = int(data[1])
    M = N * K
    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    # iterative DFS order from root 1
    parent = [0] * (M + 1)
    order = []
    visited = [False] * (M + 1)
    stack = [1]
    visited[1] = True
    while stack:
        x = stack.pop()
        order.append(x)
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                stack.append(y)
    # g[v]: 0 if closed, else length of open path ending at v (downward)
    # cnt[v]: number of open children, s1/s2 accumulate lengths
    cnt = [0] * (M + 1)
    tot = [0] * (M + 1)  # sum of open child lengths
    for x in reversed(order):
        c = cnt[x]
        if c == 0:
            g = 0 if K == 1 else 1
        elif c == 1:
            s = tot[x] + 1
            g = 0 if s == K else s
        elif c == 2:
            s = tot[x] + 1
            if s != K:
                print("No")
                return
            g = 0
        else:
            print("No")
            return
        if x == 1:
            print("Yes" if g == 0 else "No")
            return
        p = parent[x]
        if g != 0:
            cnt[p] += 1
            tot[p] += g
        # for c==1 with closed child: nothing

main()
