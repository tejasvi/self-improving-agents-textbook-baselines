import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, m, l = int(data[0]), int(data[1]), int(data[2])
    a = [int(x) for x in data[3:3 + n]]
    b = [int(x) for x in data[3 + n:3 + n + m]]
    idx = 3 + n + m
    forbidden = set()
    for _ in range(l):
        c = int(data[idx]) - 1
        d = int(data[idx + 1]) - 1
        idx += 2
        forbidden.add(c * m + d)

    order = sorted(range(m), key=lambda j: -b[j])
    best = -1
    for i in range(n):
        base = i * m
        for j in order:
            if base + j not in forbidden:
                val = a[i] + b[j]
                if val > best:
                    best = val
                break
    print(best)


main()
