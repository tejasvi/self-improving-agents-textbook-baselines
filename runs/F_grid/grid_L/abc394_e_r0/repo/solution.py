import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    grid = data[1:1 + n]

    # out[b] = list of (y, c): edge b -> y labeled c
    # inn[x][c] = list of x0: edge x0 -> x labeled c
    out = [[] for _ in range(n)]
    inn = [[[] for _ in range(26)] for _ in range(n)]
    for x in range(n):
        row = grid[x]
        for y in range(n):
            ch = row[y]
            if ch != '-':
                c = ord(ch) - 97
                out[x].append((y, c))
                inn[y][c].append(x)

    # State P(x, y): left walk currently ends at x, right walk starts at y
    # (walk from y to j). Each pair of matching edges costs 2 total.
    #   d(P(x,y)) = 1 + d(M(x', y, c))  for edge x -> x' labeled c
    #   d(M(x', y, c)) = 1 + d(P(x', y')) for edge y' -> y labeled c
    # Terminals: P(x,x) with d=0 (even palindrome), P(x,y) with edge x->y d=1.
    # Multi-source BFS on the reversed graph gives d(P(i,j)) = answer for (i,j).
    distP = [[-1] * n for _ in range(n)]
    seenM = [[[False] * 26 for _ in range(n)] for _ in range(n)]

    for x in range(n):
        distP[x][x] = 0
    frontier = [(0, x, x) for x in range(n)]
    pending = [(x, y) for x in range(n) for y, _ in out[x] if y != x]

    level = 0
    while frontier or pending:
        nxt = []
        for tag, a, b in frontier:
            if tag == 0:
                # P(a, b) -> M(a, y, c) for edge b -> y labeled c
                for y, c in out[b]:
                    if not seenM[a][y][c]:
                        seenM[a][y][c] = True
                        nxt.append((1, a, y * 26 + c))
            else:
                # M(a, y, c) -> P(x0, y) for edge x0 -> a labeled c
                y, c = divmod(b, 26)
                for x0 in inn[a][c]:
                    if distP[x0][y] < 0:
                        distP[x0][y] = level + 1
                        nxt.append((0, x0, y))
        level += 1
        if pending:
            for x, y in pending:
                if distP[x][y] < 0:
                    distP[x][y] = 1
                    nxt.append((0, x, y))
            pending = []
        frontier = nxt

    sys.stdout.write('\n'.join(' '.join(map(str, row)) for row in distP) + '\n')


main()
