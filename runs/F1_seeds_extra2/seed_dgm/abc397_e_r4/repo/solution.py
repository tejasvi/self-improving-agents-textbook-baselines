import sys
from collections import deque

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
    parent = [0] * (M + 1)
    order = []
    visited = [False] * (M + 1)
    visited[1] = True
    dq = deque([1])
    while dq:
        x = dq.popleft()
        order.append(x)
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                dq.append(y)
    # open[v]: length of open path from v downward (K means closed)
    val = [0] * (M + 1)
    # for each vertex, collect open children lengths
    short_cnt = [0] * (M + 1)
    short_sum = [0] * (M + 1)
    short_list = [[] for _ in range(M + 1)]
    for v in reversed(order):
        s = short_cnt[v]
        if s > 2:
            print("No"); return
        if s == 0:
            r = 1
        elif s == 1:
            r = short_list[v][0] + 1
        else:
            r = short_list[v][0] + short_list[v][1] + 1
            if r > K:
                print("No"); return
        if r > K:
            print("No"); return
        if v == 1:
            if r != K:
                print("No"); return
            break
        val[v] = r
        if r < K:
            p = parent[v]
            short_cnt[p] += 1
            if len(short_list[p]) < 3:
                short_list[p].append(r)
    print("Yes")

main()
