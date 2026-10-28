class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Find the last occurrence of each number
        last_occurrence = {}
        for i in range(n):
            last_occurrence[nums[i]] = i
        
        # Count the number of valid partition points
        # A partition can be made after index i if i is the maximum of all 
        # last occurrences of elements in nums[0:i+1]
        partition_count = 0
        max_last_occurrence = 0
        
        for i in range(n - 1):  # We don't count the last position
            max_last_occurrence = max(max_last_occurrence, last_occurrence[nums[i]])
            # We can make a partition after position i if i == max_last_occurrence
            if i == max_last_occurrence:
                partition_count += 1
        
        # If there are k partition points, we have 2^k ways to form good partitions
        # (either make a partition at that point or not)
        return pow(2, partition_count, MOD)
