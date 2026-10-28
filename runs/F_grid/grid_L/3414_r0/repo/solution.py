from functools import lru_cache


class Solution:
    def waysToReachStair(self, k: int) -> int:
        # Once Alice is above stair k + 1, she can never come back down to k
        # (downs cannot be consecutive and every up moves her further away),
        # so such states contribute nothing.
        @lru_cache(maxsize=None)
        def dfs(stair: int, jump: int, can_down: bool) -> int:
            if stair > k + 1:
                return 0
            res = 1 if stair == k else 0
            if can_down and stair > 0:
                res += dfs(stair - 1, jump, False)
            # 2^jump grows fast, so this step only matters while stair stays small
            res += dfs(stair + (1 << jump), jump + 1, True)
            return res

        return dfs(1, 0, True)
