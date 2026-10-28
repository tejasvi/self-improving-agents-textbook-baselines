from typing import List


class Solution:
    def findAnswer(self, parent: List[int], s: str) -> List[bool]:
        n = len(parent)
        children = [[] for _ in range(n)]
        for i in range(1, n):
            children[parent[i]].append(i)  # increasing order by construction

        # Iterative post-order traversal (children visited in increasing order).
        post_order = []
        stack = [(0, 0)]
        while stack:
            node, idx = stack.pop()
            if idx < len(children[node]):
                stack.append((node, idx + 1))
                stack.append((children[node][idx], 0))
            else:
                post_order.append(node)

        pos = [0] * n
        for p, node in enumerate(post_order):
            pos[node] = p

        size = [1] * n
        for node in post_order:  # children precede parents in post-order
            if parent[node] != -1:
                size[parent[node]] += size[node]

        P = [s[node] for node in post_order]

        # Manacher on transformed string T = #P0#P1#...#
        m = 2 * n + 1
        T = [None] * m
        for i in range(n):
            T[2 * i + 1] = P[i]
        rad = [0] * m
        lo = hi = -1  # current rightmost palindrome [lo, hi] in T
        for i in range(m):
            if i <= hi:
                k = min(rad[lo + hi - i], hi - i)
            else:
                k = 0
            while i - k - 1 >= 0 and i + k + 1 < m and T[i - k - 1] == T[i + k + 1]:
                k += 1
            rad[i] = k
            if i + k > hi:
                lo, hi = i - k, i + k

        answer = [False] * n
        for x in range(n):
            l = pos[x] - size[x] + 1
            r = pos[x]
            c = l + r + 1  # center index in T
            answer[x] = rad[c] >= r - l + 1
        return answer
