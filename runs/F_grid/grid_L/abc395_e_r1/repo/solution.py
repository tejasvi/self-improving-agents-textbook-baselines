import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n, m, x = int(data[0]), int(data[1]), int(data[2])
    # Node id: v for normal orientation, v + n for reversed orientation.
    fwd = [[] for _ in range(n)]  # original u -> v, used in normal state
    rev = [[] for _ in range(n)]  # original v -> u, used in reversed state
    idx = 3
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        fwd[u].append(v)
        rev[v].append(u)

    INF = float("inf")
    dist = [INF] * (2 * n)
    dist[0] = 0
    pq = [(0, 0)]
    target = n - 1
    while pq:
        d, s = heapq.heappop(pq)
        if d != dist[s]:
            continue
        if s == target or s == target + n:
            print(d)
            return
        if s < n:
            v, off, nbrs = s, 0, fwd[s]
        else:
            v, off, nbrs = s - n, n, rev[s - n]
        nd = d + 1
        for u in nbrs:
            t = u + off
            if nd < dist[t]:
                dist[t] = nd
                heapq.heappush(pq, (nd, t))
        nd = d + x
        t = v + (n - off)
        if nd < dist[t]:
            dist[t] = nd
            heapq.heappush(pq, (nd, t))


if __name__ == "__main__":
    main()
