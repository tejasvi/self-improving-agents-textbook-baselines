import sys, heapq

def main():
    data = sys.stdin.buffer.read().split()
    n, m, x = int(data[0]), int(data[1]), int(data[2])
    # state id: v*2 + f, f=0 normal, f=1 reversed
    adj = [[] for _ in range(2 * n)]
    idx = 3
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        # normal: u -> v along original direction
        adj[2 * u].append(2 * v)
        # reversed: traverse original edge backward v -> u
        adj[2 * v + 1].append(2 * u + 1)
    INF = float('inf')
    dist = [INF] * (2 * n)
    dist[0] = 0
    pq = [(0, 0)]
    target = 2 * (n - 1)
    while pq:
        d, s = heapq.heappop(pq)
        if d > dist[s]:
            continue
        if s == target or s == target + 1:
            print(d)
            return
        v = s >> 1
        # move along an edge (cost 1), same flag
        nd = d + 1
        for t in adj[s]:
            if nd < dist[t]:
                dist[t] = nd
                heapq.heappush(pq, (nd, t))
        # flip (cost X)
        t = s ^ 1
        nd = d + x
        if nd < dist[t]:
            dist[t] = nd
            heapq.heappush(pq, (nd, t))
    print(min(dist[target], dist[target + 1]))

main()
