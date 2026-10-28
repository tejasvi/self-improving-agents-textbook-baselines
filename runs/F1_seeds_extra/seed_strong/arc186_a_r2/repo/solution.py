import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); q = int(data[1])
    ks = [int(x) for x in data[2:2 + q]]
    M = n * n
    # reach[r][c]: bitmask of achievable free-cell counts using exactly r rows, c cols
    # in disjoint blocks a x b (a,b >= 2).
    reach = [[0] * (n + 1) for _ in range(n + 1)]
    reach[0][0] = 1
    for r in range(n + 1):
        for c in range(n + 1):
            cur = reach[r][c]
            if not cur:
                continue
            for a in range(2, n - r + 1):
                for b in range(2, n - c + 1):
                    reach[r + a][c + b] |= cur << (a * b)
    total = 0
    for r in range(n + 1):
        for c in range(n + 1):
            total |= reach[r][c]
    out = []
    for k in ks:
        f = M - k
        if 0 <= f <= M and (total >> f) & 1:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")

main()
