# Snowflake Tree solution
# We need to keep the maximum number of vertices that can form a Snowflake Tree.
# A Snowflake Tree consists of a centre vertex C, x (>=1) middle vertices each adjacent to C,
# and each middle vertex has y (>=1) leaf vertices attached to it (leaves are degree 1).
# For a chosen centre C, a neighbour V can serve as a middle vertex. The number of leaves V can
# provide is its degree minus 1 (all neighbours except C). By selecting x middle vertices with
# capacities caps_i, the feasible y is the minimum of the selected caps (the i‑th largest after
# sorting descending). The total kept vertices = 1 (centre) + x (middle) + x*y = 1 + x*(y+1).
# For each centre we evaluate all possible x by sorting capacities descending and taking
#   keep = 1 + max_{i}( i * (caps[i-1] + 1) ).
# The answer is N - max_keep over all centres.

import sys

def solve():
    sys.setrecursionlimit(1_000_000)
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    adj = [[] for _ in range(N)]
    for _ in range(N - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(adj[i]) for i in range(N)]
    max_keep = 0
    for c in range(N):
        caps = []
        for v in adj[c]:
            cap = deg[v] - 1  # neighbours of v other than centre can become leaves
            if cap > 0:
                caps.append(cap)
        if not caps:
            continue
        caps.sort(reverse=True)
        best = 0
        for i, val in enumerate(caps, start=1):  # i middle vertices chosen
            cur = i * (val + 1)  # i middle + i*val leaves
            if cur > best:
                best = cur
        total_keep = 1 + best  # include centre
        if total_keep > max_keep:
            max_keep = total_keep
    # In case no centre with caps found (e.g., N=1?), keep at least 1
    if max_keep == 0:
        max_keep = 1
    ans = N - max_keep
    print(ans)

if __name__ == "__main__":
    solve()
