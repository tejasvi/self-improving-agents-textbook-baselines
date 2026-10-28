class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def count_partitions(string: str, k: int) -> int:
            """Count partitions for a given string with at most k distinct characters"""
            partitions = 0
            i = 0
            while i < len(string):
                # Find longest prefix with at most k distinct characters
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
                
                # Move to next part
                i = j
                partitions += 1
            
            return partitions
        
        # Try without changing anything
        max_partitions = count_partitions(s, k)
        
        # Try changing each position to each character
        for i in range(len(s)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                # Skip if it's the same character
                if s[i] == c:
                    continue
                
                # Create modified string
                modified = s[:i] + c + s[i+1:]
                
                # Count partitions for modified string
                partitions = count_partitions(modified, k)
                
                # Update maximum
                max_partitions = max(max_partitions, partitions)
        
        return max_partitions
