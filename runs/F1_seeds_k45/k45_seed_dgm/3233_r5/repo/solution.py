class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def count_partitions(s: str) -> int:
            """Count the number of partitions for a given string."""
            if not s:
                return 0
            
            partitions = 0
            i = 0
            
            while i < len(s):
                # Count distinct characters in the current prefix
                char_set = set()
                j = i
                
                # Extend the prefix as long as we have at most k distinct characters
                while j < len(s) and (s[j] in char_set or len(char_set) < k):
                    char_set.add(s[j])
                    j += 1
                
                # We found a partition from i to j-1
                partitions += 1
                i = j
            
            return partitions
        
        # Start with no change
        max_partitions = count_partitions(s)
        
        # Try changing each position to each lowercase letter
        for i in range(len(s)):
            original_char = s[i]
            
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != original_char:  # Only consider actual changes
                    # Create modified string
                    modified_s = s[:i] + c + s[i+1:]
                    
                    # Count partitions and update max
                    partitions = count_partitions(modified_s)
                    max_partitions = max(max_partitions, partitions)
        
        return max_partitions
