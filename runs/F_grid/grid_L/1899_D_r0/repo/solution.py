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
        # Map byte tokens to integer counts keyed by value
        c = Counter()
        for k, v in cnt.items():
            c[int(k)] += v
        ans = 0
        for v in c.values():
            ans += v * (v - 1) // 2
        # x/2^x is equal for x=1 and x=2 (both 1/2), so pairs (1,2) also work
        ans += c.get(1, 0) * c.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
