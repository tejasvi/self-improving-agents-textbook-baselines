import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    xs = [int(v) for v in data[2:2 + m]]

    # Bridge i (1-indexed) connects i and i+1; bridge n connects n and 1.
    # For pair (a, b) with a < b: arc1 uses bridges a..b-1 (length d1 = b-a),
    # arc2 uses the other bridges (length d2 = n - d1).
    # Closing bridge i forces arc2 if i is in arc1, otherwise arc1.
    base = 0
    diff = [0] * (n + 2)
    for k in range(m - 1):
        a, b = xs[k], xs[k + 1]
        if a > b:
            a, b = b, a
        d1 = b - a
        d2 = n - d1
        base += d1
        delta = d2 - d1
        diff[a] += delta
        diff[b] -= delta  # range [a, b-1]

    best = None
    cur = 0
    for i in range(1, n + 1):
        cur += diff[i]
        total = base + cur
        if best is None or total < best:
            best = total
    print(best)


if __name__ == "__main__":
    main()
