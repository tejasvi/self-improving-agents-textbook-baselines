from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        arr = list(nums)
        tree = [0] * (n + 1)

        def add(i: int, delta: int) -> None:
            i += 1
            while i <= n:
                tree[i] += delta
                i += i & (-i)

        def prefix(i: int) -> int:
            # sum of peak flags over indices [0, i]
            i += 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        def is_peak(i: int) -> int:
            return 1 if arr[i - 1] < arr[i] > arr[i + 1] else 0

        flag = [0] * n
        for i in range(1, n - 1):
            if is_peak(i):
                flag[i] = 1
                add(i, 1)

        answer = []
        for q in queries:
            if q[0] == 1:
                lo, hi = q[1] + 1, q[2] - 1
                if lo > hi:
                    answer.append(0)
                else:
                    answer.append(prefix(hi) - prefix(lo - 1))
            else:
                idx, val = q[1], q[2]
                arr[idx] = val
                for p in (idx - 1, idx, idx + 1):
                    if 1 <= p <= n - 2:
                        new = is_peak(p)
                        if new != flag[p]:
                            add(p, new - flag[p])
                            flag[p] = new
        return answer
