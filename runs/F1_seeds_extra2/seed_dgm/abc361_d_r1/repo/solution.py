import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    if sorted(s) != sorted(t):
        print(-1)
        return
    start = s + '..'
    goal = t + '..'
    if start == goal:
        print(0)
        return

    # The two empty cells are always adjacent (invariant), so the empty
    # pair is at (k, k+1) where k is the first '.'.
    def neighbors(state):
        k = state.index('.')
        res = []
        for x in range(n + 1):
            if state[x] == '.' or state[x + 1] == '.':
                continue
            L = list(state)
            a, b = L[x], L[x + 1]
            L[x] = '.'
            L[x + 1] = '.'
            L[k] = a
            L[k + 1] = b
            res.append(''.join(L))
        return res

    # Bidirectional BFS. Moves are reversible, so the graph is undirected.
    dist_a = {start: 0}
    dist_b = {goal: 0}
    front_a = [start]
    front_b = [goal]
    da = 0  # depth of front_a
    db = 0  # depth of front_b
    best = None
    while front_a and front_b:
        if best is not None and da + db >= best:
            break
        # expand the smaller frontier
        if len(front_a) <= len(front_b):
            cur, dist_cur, dist_oth = front_a, dist_a, dist_b
            d = da
            side = 'a'
        else:
            cur, dist_cur, dist_oth = front_b, dist_b, dist_a
            d = db
            side = 'b'
        nxt = []
        for st in cur:
            for nb in neighbors(st):
                if nb not in dist_cur:
                    dist_cur[nb] = d + 1
                    nxt.append(nb)
                    if nb in dist_oth:
                        cand = d + 1 + dist_oth[nb]
                        if best is None or cand < best:
                            best = cand
        if side == 'a':
            front_a = nxt
            da += 1
        else:
            front_b = nxt
            db += 1
    print(best if best is not None else -1)


main()
