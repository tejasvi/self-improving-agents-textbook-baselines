import sys

def achievable_fixed(N):
    # reach[r][c]: bitmask of achievable non-fixed areas using exactly r rows, c cols
    # (blocks a x b with a,b >= 2, disjoint row and column sets)
    reach = [[0] * (N + 1) for _ in range(N + 1)]
    reach[0][0] = 1
    for r in range(N + 1):
        for c in range(N + 1):
            cur = reach[r][c]
            if not cur:
                continue
            for a in range(2, N - r + 1):
                for b in range(2, N - c + 1):
                    reach[r + a][c + b] |= cur << (a * b)
    nonfixed = 0
    for r in range(N + 1):
        for c in range(N + 1):
            nonfixed |= reach[r][c]
    # fixed = N*N - nonfixed
    fixed = set()
    for area in range(N * N + 1):
        if (nonfixed >> area) & 1:
            fixed.add(N * N - area)
    return fixed

def main():
    data = sys.stdin.read().split()
    N, Q = int(data[0]), int(data[1])
    ks = [int(x) for x in data[2:2 + Q]]
    ok = achievable_fixed(N)
    print("\n".join("Yes" if k in ok else "No" for k in ks))

if __name__ == "__main__":
    main()
