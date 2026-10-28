import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # 1-indexed positions
    ones = []
    twos = []
    slashes = []
    for i, ch in enumerate(s, 1):
        if ch == '1':
            ones.append(i)
        elif ch == '2':
            twos.append(i)
        else:
            slashes.append(i)
    # prefix counts of ones: pre1[i] = number of ones in positions 1..i
    pre1 = [0] * (n + 1)
    for i in range(1, n + 1):
        pre1[i] = pre1[i - 1] + (1 if s[i - 1] == '1' else 0)
    tot2 = len(twos)
    # pre2[i] = number of twos in positions 1..i
    pre2 = [0] * (n + 1)
    for i in range(1, n + 1):
        pre2[i] = pre2[i - 1] + (1 if s[i - 1] == '2' else 0)
    LO = len(ones)

    def slash_in(x, y):
        if x > y:
            return False
        i = bisect_left(slashes, x)
        return i < len(slashes) and slashes[i] <= y

    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx])
        R = int(data[idx + 1])
        idx += 2
        if not slash_in(L, R):
            out.append(0)
            continue
        a = pre1[L - 1]              # ones before L
        b = tot2 - pre2[R]           # twos after R
        ub = min(LO - a, tot2 - b)   # max possible k
        lo_k, hi_k = 0, ub
        # find max feasible k; k=0 is feasible (slash exists)
        while lo_k < hi_k:
            mid = (lo_k + hi_k + 1) // 2
            # need slash m with ones[a+mid-1] < m < twos[tot2-b-mid]
            left = ones[a + mid - 1]
            right = twos[tot2 - b - mid]
            x = max(left + 1, L)
            y = min(right - 1, R)
            if slash_in(x, y):
                lo_k = mid
            else:
                hi_k = mid - 1
        out.append(2 * lo_k + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
