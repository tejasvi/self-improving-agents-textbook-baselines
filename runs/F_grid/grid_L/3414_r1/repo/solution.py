from functools import lru_cache


class Solution:
    def waysToReachStair(self, k: int) -> int:
        # Jumps are used in order 0, 1, 2, ..., so up-moves are 2^0, 2^1, ...
        # Stairs above k + 1 can never return to k, so prune them.
        import sys
        sys.setrecursionlimit(10000)

        @lru_cache(maxsize=None)
        def dfs(stair: int, jump: int, can_down: bool) -> int:
            if stair > k + 1:
                return 0
            total = 1 if stair == k else 0
            # Go down (not consecutively, not from stair 0)
            if can_down and stair > 0:
                total += dfs(stair - 1, jump, False)
            # Go up
            total += dfs(stair + (1 << jump), jump + 1, True)
            return total

        return dfs(1, 0, True)
