from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 30) - 1

        def feasible(allowed: int) -> bool:
            # Partition nums into minimal number of contiguous segments whose AND
            # is a submask of `allowed`. Operations used = n - segments.
            segs = 0
            cur = FULL
            for x in nums:
                cur &= x
                if cur & ~allowed == 0:
                    segs += 1
                    cur = FULL
            if segs == 0:
                return False
            # Leftover trailing elements get merged into the last segment (AND only shrinks).
            return n - segs <= k

        forbidden = 0
        for b in range(29, -1, -1):
            nf = forbidden | (1 << b)
            if feasible(FULL ^ nf):
                forbidden = nf
        return FULL ^ forbidden


if __name__ == "__main__":
    s = Solution()
    print(s.minOrAfterOperations([3, 5, 3, 2, 7], 2))   # 3
    print(s.minOrAfterOperations([7, 3, 15, 14, 2, 8], 4))  # 2
    print(s.minOrAfterOperations([10, 7, 10, 3, 9, 14, 9, 4], 1))  # 15
