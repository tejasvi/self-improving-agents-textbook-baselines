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
        arr = data[pos:pos + n]
        pos += n
        cnt = Counter(arr)
        # a_i / 2^{a_i} equal iff a_i == a_j, except 1 and 2 which tie.
        total = 0
        for v in cnt.values():
            total += v * (v - 1) // 2
        c1 = cnt.get(b"1", 0)
        c2 = cnt.get(b"2", 0)
        total += c1 * c2
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
