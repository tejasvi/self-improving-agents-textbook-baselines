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
        cnt = Counter(data[pos:pos + n])
        pos += n
        # Equal exponents always work; the only distinct pair with
        # a/2^a == b/2^b is {1, 2}.
        total = 0
        for c in cnt.values():
            total += c * (c - 1) // 2
        total += cnt.get(b"1", 0) * cnt.get(b"2", 0)
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
