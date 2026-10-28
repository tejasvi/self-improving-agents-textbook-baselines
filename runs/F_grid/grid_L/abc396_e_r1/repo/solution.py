import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        x = int(data[idx]); y = int(data[idx + 1]); z = int(data[idx + 2])
        idx += 3
        adj[x].append((y, z))
        adj[y].append((x, z))

    d = [-1] * (n + 1)
    A = [0] * (n + 1)
    BITS = 31
    for s in range(1, n + 1):
        if d[s] != -1:
            continue
        d[s] = 0
        comp = [s]
        dq = deque([s])
        while dq:
            u = dq.popleft()
            du = d[u]
            for v, z in adj[u]:
                want = du ^ z
                if d[v] == -1:
                    d[v] = want
                    comp.append(v)
                    dq.append(v)
                elif d[v] != want:
                    print(-1)
                    return
        size = len(comp)
        vals = [d[v] for v in comp]
        r = 0
        for b in range(BITS):
            cnt = 0
            for x in vals:
                cnt += (x >> b) & 1
            if cnt * 2 > size:
                r |= 1 << b
        for v in comp:
            A[v] = d[v] ^ r

    sys.stdout.write(" ".join(map(str, A[1:])) + "\n")


main()
