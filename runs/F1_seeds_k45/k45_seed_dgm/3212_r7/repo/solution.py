class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        seen = set()
        result = 1
        
        for num in nums:
            if num in seen:
                # We must partition here
                # Reset the seen set to track the new partition
                seen = set()
            
            seen.add(num)
            
            # Check if this is a point where we can optionally partition
            # We can partition after any position where the next element
            # hasn't been seen yet in current partition
            # Actually, we need to check if all future elements haven't appeared yet
            # That's too expensive. Let me reconsider...
        
        # Let me reconsider the approach
        # We need to find all positions where we MUST partition
        # Then between these mandatory points, we can choose freely
        
        MOD = 10**9 + 7
        seen = set()
        mandatory_partitions = []
        
        for i, num in enumerate(nums):
            if num in seen:
                # We must partition before this element
                mandatory_partitions.append(i)
                seen = set()
            
            seen.add(num)
        
        # Number of positions where we can optionally partition
        # is len(nums) - 1 - len(mandatory_partitions)
        # But we need to be more careful
        
        # Actually, let me reconsider the mandatory partition idea
        # When we see a duplicate, we must start a new partition AT that position
        # Between mandatory positions, we have freedom
        
        # Better approach:
        # The answer is 2^(number of optional partition points)
        
        # Let's think of it differently:
        # We can only partition at position i if nums[i] has not appeared
        # in the current partition yet
        
        # Actually the key insight is:
        # - Some positions MUST be partition points (after a duplicate is encountered)
        # - Other positions CAN be partition points
        # - The answer is 2^(number of positions that can be partition points)
        
        seen = set()
        optional_partitions = 0
        
        for i in range(len(nums) - 1):  # -1 because we can't partition after the last element
            num = nums[i]
            
            if num in seen:
                # We MUST partition here, reset seen
                seen = set()
            
            seen.add(num)
            
            # Check if the next element (nums[i+1]) is new
            if nums[i+1] not in seen:
                # We can optionally partition between i and i+1
                optional_partitions += 1
        
        return pow(2, optional_partitions, MOD)
