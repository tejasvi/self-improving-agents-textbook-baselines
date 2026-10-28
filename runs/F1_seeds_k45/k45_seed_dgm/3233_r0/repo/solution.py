class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def count_partitions(string):
            """Count the number of partitions for a given string."""
            partitions = 0
            char_count = {}
            i = 0
            while i < len(string):
                # Build the longest prefix with at most k distinct characters
                char_count.clear()
                j = i
                while j < len(string):
                    if string[j] not in char_count:
                        if len(char_count) == k:
                            # Can't add more distinct characters
                            break
                        char_count[string[j]] = 0
                    char_count[string[j]] += 1
                    j += 1
                
                # We found a partition from i to j-1
                partitions += 1
                i = j
            
            return partitions
        
        # Calculate partitions without any change
        max_partitions = count_partitions(s)
        
        # Try changing each character to every possible letter
        for i in range(len(s)):
            original_char = s[i]
            for new_char in 'abcdefghijklmnopqrstuvwxyz':
                if new_char == original_char:
                    continue
                # Change character at position i
                modified_s = s[:i] + new_char + s[i+1:]
                partitions = count_partitions(modified_s)
                max_partitions = max(max_partitions, partitions)
        
        return max_partitions
