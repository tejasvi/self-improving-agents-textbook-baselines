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
        cnt = {int(k): v for k, v in cnt.items()}
        ans = 0
        for v in cnt.values():
            ans += v * (v - 1) // 2
        ans += cnt.get(1, 0) * cnt.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
