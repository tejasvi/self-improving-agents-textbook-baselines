import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] + [int(x) for x in data[1:1 + n]]

    # L[i]: distinct count in A[1..i]
    L = [0] * (n + 2)
    seen = bytearray(n + 2)
    c = 0
    for i in range(1, n + 1):
        if not seen[A[i]]:
            seen[A[i]] = 1
            c += 1
        L[i] = c

    # R[j]: distinct count in A[j..n]
    R = [0] * (n + 3)
    seen = bytearray(n + 2)
    c = 0
    for j in range(n, 0, -1):
        if not seen[A[j]]:
            seen[A[j]] = 1
            c += 1
        R[j] = c

    # prev occurrence
    prev = [0] * (n + 2)
    last_pos = [0] * (n + 2)
    for j in range(1, n + 1):
        prev[j] = last_pos[A[j]]
        last_pos[A[j]] = j

    parent = list(range(n + 3))  # DSU: next alive position >= x
    prv = [0] * (n + 2)          # previous alive stack element (0 = none)
    d = [0] * (n + 2)            # v_p - v_next(p) for alive non-last p

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    ans = 0
    last = 0   # newest alive element (0 = empty stack)
    V = 0      # value of last element
    S = 0      # sum of d = v_head - V
    for j in range(2, n):
        w = L[j - 1]
        # append position j with value w, popping dominated tail elements
        while last != 0 and V <= w:
            p = prv[last]
            parent[last] = last + 1
            if p == 0:
                last = 0
                S = 0
                break
            V += d[p]
            S -= d[p]
            last = p
        if last != 0:
            d[last] = V - w
            S += d[last]
        prv[j] = last
        last = j
        V = w
        # suffix add +1 on positions [max(prev_j+1, 2), j]
        x = prev[j] + 1
        if x < 2:
            x = 2
        k = find(x)
        V += 1
        p = prv[k]
        if p:
            d[p] -= 1
            S -= 1
            if d[p] == 0:
                prv[k] = prv[p]
                parent[p] = p + 1
        if j <= n - 1:
            cand = V + S + R[j + 1]
            if cand > ans:
                ans = cand
    print(ans)


main()
