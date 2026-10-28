import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] + [int(x) for x in data[1:1 + n]]  # 1-indexed

    # L[i] = distinct count in A[1..i]
    L = [0] * (n + 2)
    seen = set()
    for i in range(1, n + 1):
        seen.add(A[i])
        L[i] = len(seen)
    # R[k] = distinct count in A[k..n]
    R = [0] * (n + 2)
    seen = set()
    for k in range(n, 0, -1):
        seen.add(A[k])
        R[k] = len(seen)
    # prev occurrence index (0 if none)
    prev = [0] * (n + 1)
    last = {}
    for i in range(1, n + 1):
        prev[i] = last.get(A[i], 0)
        last[A[i]] = i

    # For fixed j: V[i] = L[i] + distinct(A[i+1..j]), 1 <= i <= j-1.
    # Step j-1 -> j: V[i] += 1 for i in [prev[j], j-1] (suffix).
    # Survivors have strictly decreasing V left to right (an earlier index
    # with V >= a later one is dominated forever, since increments are
    # suffixes). Head = max. Answer(j) = V[head] + R[j+1].
    parent = list(range(n + 2))  # DSU: smallest alive index >= x
    prv = [-1] * (n + 2)
    diff = [0] * (n + 2)         # diff[k] = V[prv[k]] - V[k] > 0
    tail = -1
    tailval = 0
    headval = 0
    best = 0

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            nx = parent[x]
            parent[x] = root
            x = nx
        return root

    for j in range(2, n):
        i = j - 1
        v = L[i]  # new candidate, middle still empty
        while tail != -1 and tailval <= v:
            t = tail
            parent[t] = t + 1
            tailval += diff[t]
            tail = prv[t]
        if tail == -1:
            prv[i] = -1
            headval = v
        else:
            prv[i] = tail
            diff[i] = tailval - v
        tail = i
        tailval = v

        pv = prev[j]
        p = pv if pv >= 1 else 1
        k = find(p)
        if k <= tail:
            tailval += 1
            a = prv[k]
            if a == -1:
                headval += 1
            else:
                diff[k] -= 1
                if diff[k] == 0:
                    # V[a] == V[k]: a is dominated, remove it
                    parent[a] = a + 1
                    b = prv[a]
                    prv[k] = b
                    if b != -1:
                        diff[k] = diff[a]
                    # if b == -1, a was head; V[k] == V[a] == headval now

        cand = headval + R[j + 1]
        if cand > best:
            best = cand
    print(best)

main()
