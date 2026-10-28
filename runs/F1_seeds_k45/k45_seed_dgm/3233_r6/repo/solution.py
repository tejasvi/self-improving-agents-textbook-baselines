class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def countPartitions(string):
            """Count the number of partitions for a given string"""
            partitions = 0
            i = 0
            while i < len(string):
                # Find the longest prefix with at most k distinct characters
                char_count = {}
                j = i
                while j < len(string):
                    char = string[j]
                    if char not in char_count:
                        if len(char_count) == k:
                            # Can't add more distinct characters
                            break
                        char_count[char] = 0
                    char_count[char] += 1
                    j += 1
                # j is now the index right after the last character we can include
                partitions += 1
                i = j
            return partitions
        
        max_partitions = countPartitions(s)
        
        # Try changing each position
        for i in range(len(s)):
            original_char = s[i]
            # Try changing to each lowercase letter
            for new_char in 'abcdefghijklmnopqrstuvwxyz':
                if new_char == original_char:
                    continue
                # Create modified string
                modified = s[:i] + new_char + s[i+1:]
                partitions = countPartitions(modified)
                max_partitions = max(max_partitions, partitions)
        
        return max_partitions
