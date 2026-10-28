import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    # nge[i]: next greater index (0 if none); cnt[i]: number of chain nodes from i (inclusive)
    nge = [0] * (n + 2)
    cnt = [0] * (n + 2)
    st = []
    for i in range(n, 0, -1):
        h = H[i]
        while st and H[st[-1]] < h:
            st.pop()
        if st:
            nge[i] = st[-1]
            cnt[i] = cnt[st[-1]] + 1
        else:
            nge[i] = 0
            cnt[i] = 1
        st.append(i)
    # group queries by r
    qs_by_r = [[] for _ in range(n + 1)]
    pos = 2 + n
    L = [0] * q
    for k in range(q):
        l = int(data[pos]); r = int(data[pos + 1]); pos += 2
        L[k] = l
        qs_by_r[r].append(k)
    ans = [0] * q
    stack = []  # indices increasing, H strictly decreasing
    for r in range(1, n + 1):
        h = H[r]
        while stack and H[stack[-1]] < h:
            stack.pop()
        stack.append(r)
        for k in qs_by_r[r]:
            l = L[k]
            m = stack[bisect_left(stack, l + 1)]  # argmax of H[l+1..r]
            p = nge[m]
            ans[k] = cnt[p] if p else 0
    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()
