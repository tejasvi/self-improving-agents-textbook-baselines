import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    # Unique keys ordering by (A_i, i)
    key = [a[i] * (n + 1) + i for i in range(n)]

    # Nearest strictly-greater key to the left / right (Cartesian tree boundaries)
    left = [-1] * n
    right = [n] * n
    stack = []
    for i in range(n):
        ki = key[i]
        while stack and key[stack[-1]] < ki:
            right[stack.pop()] = i
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    # Prefix sums
    pre = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += a[i]
        pre[i + 1] = s

    # Parent = boundary with smaller key (if any)
    # F[v] = final answer when v's whole subtree has been absorbed
    F = [0] * n
    sub_sum = [0] * n
    for v in range(n):
        sub_sum[v] = pre[right[v]] - pre[left[v] + 1]

    order = sorted(range(n), key=key.__getitem__, reverse=True)
    for v in order:
        l = left[v]
        r = right[v]
        if l < 0 and r >= n:
            parent = -1
        elif l < 0:
            parent = r
        elif r >= n:
            parent = l
        else:
            parent = l if key[l] < key[r] else r
        sv = sub_sum[v]
        if parent < 0 or a[parent] >= sv:
            F[v] = sv
        else:
            F[v] = F[parent]

    out = []
    for k in range(n):
        has_smaller = (k > 0 and a[k - 1] < a[k]) or (k < n - 1 and a[k + 1] < a[k])
        if has_smaller:
            out.append(F[k])
        else:
            out.append(a[k])
    sys.stdout.write(" ".join(map(str, out)) + "\n")


main()
