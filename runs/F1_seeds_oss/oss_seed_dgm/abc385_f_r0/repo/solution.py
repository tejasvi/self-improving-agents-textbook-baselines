# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    X = []
    H = []
    for _ in range(n):
        X.append(int(next(it)))
        H.append(int(next(it)))
    # function to check if all buildings are visible from height h at coordinate 0
    def all_visible(h: float) -> bool:
        prev = -1e100  # negative infinity
        for xi, hi in zip(X, H):
            slope = (hi - h) / xi
            # need strictly increasing slopes
            if slope <= prev:
                return False
            prev = slope
        return True

    # if already visible at height 0, answer is -1
    if all_visible(0.0):
        print(-1)
        return

    # find an upper bound where visibility holds
    lo = 0.0
    hi = max(H) + 1.0  # start with a reasonable upper bound
    while not all_visible(hi):
        hi *= 2.0
    # binary search for the smallest h where visibility becomes true
    for _ in range(80):  # enough for 1e-12 precision
        mid = (lo + hi) * 0.5
        if all_visible(mid):
            hi = mid
        else:
            lo = mid
    # lo is the maximum height where not all buildings are visible
    # output with high precision
    print("{:.15f}".format(lo))

if __name__ == "__main__":
    solve()
