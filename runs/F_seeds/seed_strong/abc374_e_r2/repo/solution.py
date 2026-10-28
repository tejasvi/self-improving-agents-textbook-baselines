import sys

def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    items = []
    idx = 2
    for _ in range(n):
        A, P, B, Q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        items.append((A, P, B, Q))

    def feasible(C):
        total = 0
        for A, P, B, Q in items:
            best = None
            # enumerate count of T machines (b < A suffices for one side of ratio)
            for b in range(A):
                rem = C - b * B
                a = 0 if rem <= 0 else -(-rem // A)
                c = a * P + b * Q
                if best is None or c < best:
                    best = c
                if rem <= 0:
                    break
            # enumerate count of S machines (a < B suffices for the other side)
            for a in range(B):
                rem = C - a * A
                b = 0 if rem <= 0 else -(-rem // B)
                c = a * P + b * Q
                if c < best:
                    best = c
                if rem <= 0:
                    break
            total += best
            if total > X:
                return False
        return True

    lo, hi = 0, 100 * X + 100  # lo always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

main()
