import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos])
        pos += 1
        cnt = Counter(map(int, data[pos:pos + n]))
        pos += n
        # Equal values always pair up; x/2^x is equal only for x=1 and x=2.
        total = 0
        for c in cnt.values():
            total += c * (c - 1) // 2
        c1 = cnt.get(1, 0)
        c2 = cnt.get(2, 0)
        total += c1 * c2
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
