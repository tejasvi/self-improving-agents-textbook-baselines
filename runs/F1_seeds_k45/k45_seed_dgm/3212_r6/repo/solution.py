class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # Find the last occurrence of each number
        last_occurrence = {}
        for i, num in enumerate(nums):
            last_occurrence[num] = i
        
        # Count valid partition points
        result = 1
        max_last = -1  # Maximum last occurrence seen so far
        
        for i in range(len(nums) - 1):  # We don't partition after the last element
            max_last = max(max_last, last_occurrence[nums[i]])
            
            # If current position is the last occurrence of all numbers seen so far
            # then we can make a partition here
            if i == max_last:
                result = (result * 2) % MOD
        
        return result
