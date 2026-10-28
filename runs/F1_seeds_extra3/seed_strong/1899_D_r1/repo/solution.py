import sys
from collections import Counter

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        cnt = Counter(data[pos:pos + n]); pos += n
        # map bytes tokens to integer values
        c = Counter()
        for k, v in cnt.items():
            c[int(k)] += v
        ans = 0
        for v in c.values():
            ans += v * (v - 1) // 2
        # a=1 and a=2 have equal x/2^x = 1/2
        ans += c.get(1, 0) * c.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")

main()
