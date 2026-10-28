import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos:pos + n]; pos += n
        P = [0] * (n + 1)
        s = 0
        for i in range(n):
            s += int(a[i])
            P[i + 1] = s
        best = 0
        # Only k dividing n yields valid partitions; sum of n/k over divisors is sigma(n).
        for k in range(1, n + 1):
            if n % k:
                continue
            sums = [P[i + k] - P[i] for i in range(0, n, k)]
            diff = max(sums) - min(sums)
            if diff > best:
                best = diff
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
