# Write your solution here. Read from stdin, write to stdout.
import sys

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline
    N_M = input().split()
    if not N_M:
        return
    N, M = map(int, N_M)
    adj = [[] for _ in range(N)]
    for _ in range(M):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * N
    components = []  # list of (cnt0, cnt1)
    from collections import deque
    for i in range(N):
        if color[i] == -1:
            dq = deque([i])
            color[i] = 0
            cnt = [0, 0]
            cnt[0] = 1
            while dq:
                v = dq.popleft()
                for nb in adj[v]:
                    if color[nb] == -1:
                        color[nb] = color[v] ^ 1
                        cnt[color[nb]] += 1
                        dq.append(nb)
                    else:
                        # given graph is bipartite, no need to check odd cycle
                        pass
            components.append((cnt[0], cnt[1]))
    # DP using bitset represented by Python int
    bitset = 1  # bit i set means sum i achievable for left side
    for a, b in components:
        # shift by a and b and OR
        bitset = (bitset << a) | (bitset << b)
    max_prod = 0
    # iterate over possible left sizes
    # bitset has bits up to N
    for left in range(N + 1):
        if (bitset >> left) & 1:
            prod = left * (N - left)
            if prod > max_prod:
                max_prod = prod
    moves = max_prod - M
    if moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == "__main__":
    main()
