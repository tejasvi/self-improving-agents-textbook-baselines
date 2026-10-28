class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def count_partitions(string: str, k: int) -> int:
            """Count the number of partitions we can make from the string."""
            partitions = 0
            i = 0
            while i < len(string):
                # Find the longest prefix with at most k distinct characters
                char_count = {}
                j = i
                while j < len(string):
                    char = string[j]
                    if char not in char_count:
                        char_count[char] = 0
                    char_count[char] += 1
                    
                    # If adding this character exceeds k distinct characters, stop
                    if len(char_count) > k:
                        break
                    j += 1
                
                # We found a partition from i to j (exclusive)
                partitions += 1
                i = j
            
            return partitions
        
        # Try not changing anything
        max_partitions = count_partitions(s, k)
        
        # Try changing each position to each letter
        for i in range(len(s)):
            original_char = s[i]
            # Try changing to each letter
            for new_char in 'abcdefghijklmnopqrstuvwxyz':
                if new_char != original_char:
                    # Create modified string
                    modified = s[:i] + new_char + s[i+1:]
                    partitions = count_partitions(modified, k)
                    max_partitions = max(max_partitions, partitions)
        
        return max_partitions
