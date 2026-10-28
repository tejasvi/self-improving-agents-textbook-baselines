import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    prev = [0] * (n + 2)
    last = {}
    for k in range(1, n + 1):
        v = a[k - 1]
        prev[k] = last.get(v, 0)
        last[v] = k
    # L[i] = distinct in a[1..i]
    L = [0] * (n + 1)
    seen = set()
    for i in range(1, n + 1):
        seen.add(a[i - 1])
        L[i] = len(seen)
    # R[j] = distinct in a[j+1..n]
    R = [0] * (n + 2)
    seen = set()
    for j in range(n, 0, -1):
        R[j] = len(seen)
        seen.add(a[j - 1])

    # Candidates i (1-indexed) with V[i] = L[i] + distinct(a[i+1..j]).
    # Stack keeps strictly decreasing values; diff[c] = V[prv[c]] - V[c].
    parent = list(range(n + 2))  # DSU: smallest alive index >= x

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    prv = [-1] * (n + 2)
    diff = [0] * (n + 2)
    tail = -1
    tailVal = 0
    maxVal = 0  # value of bottom of stack = global max
    best = 0
    for j in range(2, n):
        i = j - 1
        x = L[i]
        # pop dominated tail entries (value <= x)
        while tail != -1 and tailVal <= x:
            t = tail
            parent[t] = t + 1
            if prv[t] == -1:
                tail = -1
                tailVal = 0
                break
            tailVal += diff[t]
            tail = prv[t]
        if tail == -1:
            prv[i] = -1
            maxVal = x
        else:
            prv[i] = tail
            diff[i] = tailVal - x
        tail = i
        tailVal = x
        # a[j] adds +1 to V[k] for k in [max(prev[j],1), j-1]
        q = prev[j]
        if q < 1:
            q = 1
        c = find(q)
        tailVal += 1
        if prv[c] == -1:
            maxVal += 1
        else:
            diff[c] -= 1
            if diff[c] == 0:
                r = prv[c]
                parent[r] = r + 1
                if prv[r] == -1:
                    prv[c] = -1
                else:
                    diff[c] = diff[r]
                    prv[c] = prv[r]
        cand = maxVal + R[j]
        if cand > best:
            best = cand
    print(best)


main()
