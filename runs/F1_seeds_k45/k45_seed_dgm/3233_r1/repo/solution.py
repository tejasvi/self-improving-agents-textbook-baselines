class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def count_partitions(s: str, k: int) -> int:
            """Count the number of partitions for a given string."""
            partitions = 0
            i = 0
            
            while i < len(s):
                # Find the longest prefix with at most k distinct characters
                char_count = {}
                j = i
                
                while j < len(s):
                    char = s[j]
                    char_count[char] = char_count.get(char, 0) + 1
                    
                    # If we exceed k distinct characters, stop
                    if len(char_count) > k:
                        break
                    j += 1
                
                # We've found a partition from i to j
                partitions += 1
                i = j
            
            return partitions
        
        # Try original string
        max_partitions = count_partitions(s, k)
        
        # Try changing each character to each of the 26 lowercase letters
        for i in range(len(s)):
            original_char = s[i]
            for new_char in 'abcdefghijklmnopqrstuvwxyz':
                if new_char != original_char:
                    # Create modified string
                    s_list = list(s)
                    s_list[i] = new_char
                    modified_s = ''.join(s_list)
                    
                    # Count partitions for modified string
                    partitions = count_partitions(modified_s, k)
                    max_partitions = max(max_partitions, partitions)
        
        return max_partitions
