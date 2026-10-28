import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = data[1:1 + n]
    # L[i]: distinct count of A[1..i]; R[j]: distinct count of A[j..n]
    L = [0] * (n + 2)
    seen = set()
    for i in range(1, n + 1):
        seen.add(A[i - 1])
        L[i] = len(seen)
    R = [0] * (n + 2)
    seen = set()
    for j in range(n, 0, -1):
        seen.add(A[j - 1])
        R[j] = len(seen)
    prev = [0] * (n + 2)
    last_pos = {}
    for i in range(1, n + 1):
        a = A[i - 1]
        prev[i] = last_pos.get(a, 0)
        last_pos[a] = i

    # Candidates i (over indices 1..j-1) whose value v(i) is strictly greater
    # than every later value. Values: v(i) = L[i] + D(i+1..j).
    # Alive candidates form a linked list (prv pointers), diff[c] = v(prv[c]) - v(c).
    # DSU nxt: find(p) = first alive candidate index >= p (removed index -> r+1).
    parent = list(range(n + 2))
    diff = [0] * (n + 2)
    prv = [0] * (n + 2)

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    head = 0      # 0 = empty
    tail = 0
    lastval = 0   # v(tail)
    M = 0         # v(head)
    best = -1
    for j in range(2, n):
        # append candidate i = j-1 with value L[j-1] (before the +1 of element j)
        t = j - 1
        x = L[t]
        while tail and lastval <= x:
            r = tail
            parent[r] = r + 1
            if r == head:
                head = 0
                tail = 0
                break
            pr = prv[r]
            lastval += diff[r]
            tail = pr
        if head == 0:
            head = t
            tail = t
            M = x
            lastval = x
        else:
            diff[t] = lastval - x
            prv[t] = tail
            tail = t
            lastval = x
        # element j is added to D(i+1..j) for i in [prev[j], j-1]
        p = prev[j] if prev[j] > 0 else 1
        c = find(p)
        if c == head:
            M += 1
        else:
            diff[c] -= 1
            if diff[c] == 0:
                pr = prv[c]
                # remove pr; c takes its place with the same value
                parent[pr] = pr + 1
                if pr == head:
                    head = c
                    prv[c] = 0
                else:
                    diff[c] = diff[pr]
                    prv[c] = prv[pr]
        lastval += 1
        cand = M + R[j + 1]
        if cand > best:
            best = cand
    print(best)


main()
