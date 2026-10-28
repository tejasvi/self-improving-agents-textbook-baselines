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

    pot = [-1] * (n + 1)
    A = [0] * (n + 1)
    BITS = 31
    for s in range(1, n + 1):
        if pot[s] != -1:
            continue
        pot[s] = 0
        comp = [s]
        dq = deque([s])
        while dq:
            u = dq.popleft()
            pu = pot[u]
            for v, z in adj[u]:
                want = pu ^ z
                if pot[v] == -1:
                    pot[v] = want
                    comp.append(v)
                    dq.append(v)
                elif pot[v] != want:
                    print(-1)
                    return
        if len(comp) == 1:
            A[s] = 0
            continue
        vals = [pot[v] for v in comp]
        half = len(comp) / 2.0
        t = 0
        for b in range(BITS):
            cnt = 0
            for p in vals:
                cnt += (p >> b) & 1
            if cnt > half:
                t |= (1 << b)
        for v in comp:
            A[v] = pot[v] ^ t

    sys.stdout.write(" ".join(map(str, A[1:])) + "\n")


main()
