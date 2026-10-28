from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        """Return the maximum possible sum f(x) for any starting player x.

        The game follows the deterministic mapping given by ``receiver`` and the
        ball is passed exactly ``k`` times.  For a starting id ``x`` we need the
        sum of ``x`` and the ids visited during the ``k`` passes (including
        repetitions).  ``k`` can be as large as 1e10, so a naïve simulation for
        every starting point would be far too slow.

        The classic solution is binary lifting (also known as doubling).  For
        each power of two ``2^j`` we pre‑compute:

        * ``up[j][i]`` – the node reached from ``i`` after ``2^j`` steps.
        * ``sum_tab[j][i]`` – the sum of node ids visited during those ``2^j``
          steps (excluding the starting node ``i`` itself, but including the
          destination nodes).

        With these tables a query for an arbitrary ``k`` can be answered in
        ``O(log k)`` by decomposing ``k`` into binary bits and aggregating the
        pre‑computed jumps.

        Overall time complexity: ``O(n * log k)`` where ``n = len(receiver)``.
        Memory usage: ``O(n * log k)``.
        """
        n = len(receiver)
        # Number of bits needed to represent k (since k >= 1)
        LOG = k.bit_length()

        # up[j][i] – node after 2^j steps from i
        up: List[List[int]] = [[0] * n for _ in range(LOG)]
        # sum_tab[j][i] – sum of node ids visited during those 2^j steps
        sum_tab: List[List[int]] = [[0] * n for _ in range(LOG)]

        # Base: 2^0 = 1 step
        for i in range(n):
            up[0][i] = receiver[i]
            sum_tab[0][i] = receiver[i]

        # Build tables for larger powers of two
        for j in range(1, LOG):
            prev_up = up[j - 1]
            prev_sum = sum_tab[j - 1]
            cur_up = up[j]
            cur_sum = sum_tab[j]
            for i in range(n):
                mid = prev_up[i]                # node after 2^{j-1} steps
                cur_up[i] = prev_up[mid]        # node after another 2^{j-1} steps
                cur_sum[i] = prev_sum[i] + prev_sum[mid]

        # Evaluate f(x) for each possible starting player
        best = 0
        for x in range(n):
            cur = x
            total = x  # include the starting id itself
            steps = k
            bit = 0
            while steps:
                if steps & 1:
                    total += sum_tab[bit][cur]
                    cur = up[bit][cur]
                steps >>= 1
                bit += 1
            if total > best:
                best = total
        return best
