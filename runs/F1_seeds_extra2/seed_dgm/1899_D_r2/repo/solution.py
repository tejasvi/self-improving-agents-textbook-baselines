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
        # Convert keys to int-based counts (bytes keys are fine for equality
        # but 1 and 2 need numeric identification).
        c1 = cnt.get(1, 0)
        c2 = cnt.get(2, 0)
        ans = c1 * c2
        for c in cnt.values():
            ans += c * (c - 1) // 2
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
