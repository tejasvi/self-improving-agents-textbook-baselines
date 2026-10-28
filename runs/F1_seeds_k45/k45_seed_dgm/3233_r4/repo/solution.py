class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def count_partitions(s_str, k):
            """Count the number of partitions in a string following the rules"""
            partitions = 0
            i = 0
            while i < len(s_str):
                # Find the longest prefix with at most k distinct characters
                char_count = {}
                j = i
                while j < len(s_str):
                    if s_str[j] not in char_count:
                        char_count[s_str[j]] = 0
                    char_count[s_str[j]] += 1
                    
                    # If we exceed k distinct characters, stop
                    if len(char_count) > k:
                        break
                    j += 1
                
                # If we broke early because of too many distinct chars,
                # we take the prefix up to (but not including) position j
                if j < len(s_str) and len(char_count) > k:
                    j -= 1
                
                # If we have a valid prefix
                if j > i:
                    partitions += 1
                    i = j
                else:
                    # Single character that creates a new distinct character
                    partitions += 1
                    i += 1
            
            return partitions
        
        max_partitions = count_partitions(s, k)
        
        # Try changing each position to each possible character
        for i in range(len(s)):
            original_char = s[i]
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != original_char:
                    # Create new string with character changed
                    s_list = list(s)
                    s_list[i] = c
                    s_modified = ''.join(s_list)
                    
                    # Count partitions and update max
                    partitions = count_partitions(s_modified, k)
                    max_partitions = max(max_partitions, partitions)
        
        return max_partitions
