import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n, m, s, t = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    adj = [[] for _ in range(n + 1)]
    idx = 4
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)

    # BFS over joint states (a, b) with a != b; piece A starts at s, piece B at t.
    # Goal: A at t and B at s.
    goal = (t, s)
    dist = {(s, t): 0}
    q = deque([(s, t)])
    while q:
        state = q.popleft()
        a, b = state
        d = dist[state] + 1
        if state == goal:
            break
        for na in adj[a]:
            if na != b:
                ns = (na, b)
                if ns not in dist:
                    dist[ns] = d
                    q.append(ns)
        for nb in adj[b]:
            if nb != a:
                ns = (a, nb)
                if ns not in dist:
                    dist[ns] = d
                    q.append(ns)
    print(dist.get(goal, -1))


main()
