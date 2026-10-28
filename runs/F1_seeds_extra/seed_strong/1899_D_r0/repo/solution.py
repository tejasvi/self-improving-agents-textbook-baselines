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
        total = 0
        for v in cnt.values():
            total += v * (v - 1) // 2
        # x/2^x equal for x=1 and x=2
        c1 = cnt.get(1, 0)
        c2 = cnt.get(2, 0)
        total += c1 * c2
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
