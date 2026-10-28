import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, m, l = int(data[0]), int(data[1]), int(data[2])
    pos = 3
    a = [int(x) for x in data[pos:pos + n]]
    pos += n
    b = [int(x) for x in data[pos:pos + m]]
    pos += m

    banned = [set() for _ in range(n)]
    for _ in range(l):
        c = int(data[pos]) - 1
        d = int(data[pos + 1]) - 1
        pos += 2
        banned[c].add(d)

    # Side dish indices sorted by price, descending.
    order = sorted(range(m), key=lambda j: -b[j])

    best = 0
    for i in range(n):
        bi = banned[i]
        ai = a[i]
        if not bi:
            cand = ai + b[order[0]]
        else:
            cand = -1
            for j in order:
                if j not in bi:
                    cand = ai + b[j]
                    break
        if cand > best:
            best = cand
    print(best)


main()
