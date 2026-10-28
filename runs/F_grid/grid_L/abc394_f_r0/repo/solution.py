import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        deg[a] += 1
        deg[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    good = [d >= 4 for d in deg]
    seen = [False] * (n + 1)
    best = 0
    for s in range(1, n + 1):
        if good[s] and not seen[s]:
            seen[s] = True
            q = deque([s])
            cnt = 0
            while q:
                v = q.popleft()
                cnt += 1
                for w in adj[v]:
                    if good[w] and not seen[w]:
                        seen[w] = True
                        q.append(w)
            if cnt > best:
                best = cnt
    print(3 * best + 2 if best > 0 else -1)

main()
