import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [0] * (n + 2)
    for i in range(1, n + 1):
        H[i] = int(data[1 + i])
    # next greater element
    nge = [n + 1] * (n + 2)
    st = []
    for i in range(1, n + 1):
        h = H[i]
        while st and H[st[-1]] < h:
            nge[st.pop()] = i
        st.append(i)
    # g[i] = number of nge-ancestors of i
    g = [0] * (n + 2)
    for i in range(n, 0, -1):
        j = nge[i]
        g[i] = g[j] + 1 if j <= n else 0
    # group queries by r
    base = 2 + n
    byr = [[] for _ in range(n + 1)]
    for k in range(q):
        l = int(data[base + 2 * k]); r = int(data[base + 2 * k + 1])
        byr[r].append((l, k))
    ans = [0] * q
    stack = []  # indices with decreasing H, increasing index
    for r in range(1, n + 1):
        h = H[r]
        while stack and H[stack[-1]] < h:
            stack.pop()
        stack.append(r)
        for l, k in byr[r]:
            m = stack[bisect_left(stack, l + 1)]
            ans[k] = g[m]
    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()
