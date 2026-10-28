from typing import List


class Solution:
    def findAnswer(self, parent: List[int], s: str) -> List[bool]:
        n = len(parent)
        children = [[] for _ in range(n)]
        for i in range(1, n):
            children[parent[i]].append(i)  # ascending order by construction

        # Iterative postorder (children in increasing order, then node).
        order = []
        stack = [(0, 0)]
        while stack:
            node, idx = stack.pop()
            if idx < len(children[node]):
                stack.append((node, idx + 1))
                stack.append((children[node][idx], 0))
            else:
                order.append(node)

        pos = [0] * n
        for p, node in enumerate(order):
            pos[node] = p

        size = [1] * n
        for node in order:  # postorder: children come before parent
            if parent[node] != -1:
                size[parent[node]] += size[node]

        # Characters in postorder.
        seq = [s[node] for node in order]

        # Manacher on transformed string T = '#' + '#'.join(seq) + '#'.
        m = 2 * n + 1
        T = [''] * m
        for i in range(n):
            T[2 * i + 1] = seq[i]
        # d[c] = max k such that T[c-k..c+k] is a palindrome
        d = [0] * m
        center = r = 0
        for c in range(m):
            k = 0
            if c < r:
                k = min(r - c, d[2 * center - c])
            while c - k - 1 >= 0 and c + k + 1 < m and T[c - k - 1] == T[c + k + 1]:
                k += 1
            d[c] = k
            if c + k > r:
                center, r = c, c + k

        ans = [False] * n
        for x in range(n):
            L = pos[x] - size[x] + 1
            R = pos[x]
            # Substring seq[L..R] is a palindrome iff d[L+R+1] >= R-L
            ans[x] = d[L + R + 1] >= R - L
        return ans
