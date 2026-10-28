from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1

        def count(A: int, B: int) -> int:
            # number of pairs (x, y), 0<=x<=A, 0<=y<=B, x+y<=K
            A = min(A, K)
            B = min(B, K)
            t = K - B  # for x <= t, min(B, K-x) = B
            total = 0
            m = min(A, t)
            total += (m + 1) * (B + 1)
            if A > t:
                # x from t+1..A, values K-x+1 range from K-A+1 .. K-t
                lo = K - A + 1
                hi = K - t
                total += (lo + hi) * (hi - lo + 1) // 2
            return total

        def contrib(arr, strict_left_ge: bool) -> int:
            # arr values; for each i, left extent: nearest left index with
            # value >= arr[i] (if strict_left_ge) else > arr[i]; right: opposite.
            left = [0] * n
            right = [0] * n
            st = []
            for i in range(n):
                v = arr[i]
                if strict_left_ge:
                    while st and arr[st[-1]] < v:
                        st.pop()
                else:
                    while st and arr[st[-1]] <= v:
                        st.pop()
                left[i] = i - (st[-1] if st else -1)
                st.append(i)
            st = []
            for i in range(n - 1, -1, -1):
                v = arr[i]
                if strict_left_ge:
                    while st and arr[st[-1]] <= v:
                        st.pop()
                else:
                    while st and arr[st[-1]] < v:
                        st.pop()
                right[i] = (st[-1] if st else n) - i
                st.append(i)
            res = 0
            for i in range(n):
                # left[i] = a+1 choices of start, right[i] = b+1 choices of end
                res += arr[i] * count(left[i] - 1, right[i] - 1)
            return res

        # max: left uses '<' popping (prev >= v stops), right pops '<=' (next > v stops)
        mx = contrib(nums, True)
        # min: symmetric by negation
        neg = [-x for x in nums]
        mn = -contrib(neg, True)
        return mx + mn
