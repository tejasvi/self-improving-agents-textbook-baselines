class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        word_len = n + m - 1
        
        # Try to build the string greedily with backtracking
        def backtrack(word):
            # If we've built the complete word, check if it's valid
            if len(word) == word_len:
                return is_valid(word)
            
            # Try each character from 'a' to 'z'
            for c in 'abcdefghijklmnopqrstuvwxyz':
                word.append(c)
                
                # Check if current partial word can lead to a valid solution
                if can_be_valid(word):
                    result = backtrack(word)
                    if result:
                        return result
                
                word.pop()
            
            return False
        
        def is_valid(word):
            """Check if the entire word satisfies all constraints"""
            for i in range(n):
                substring = ''.join(word[i:i+m])
                if str1[i] == 'T':
                    if substring != str2:
                        return False
                else:  # str1[i] == 'F'
                    if substring == str2:
                        return False
            return True
        
        def can_be_valid(word):
            """Check if partial word can potentially lead to valid solution"""
            # For completed substrings, check constraints
            for i in range(len(word) - m + 1):
                if i + m <= len(word):
                    substring = ''.join(word[i:i+m])
                    if str1[i] == 'T':
                        if substring != str2:
                            return False
                    else:  # str1[i] == 'F'
                        if substring == str2:
                            return False
            
            # Also check if we're forced to match/not match in the future
            # For indices where we can fully determine the substring constraint
            for i in range(n):
                if i + m <= len(word):
                    # Full substring is known
                    substring = ''.join(word[i:i+m])
                    if str1[i] == 'T' and substring != str2:
                        return False
                    if str1[i] == 'F' and substring == str2:
                        return False
            
            return True
        
        result = backtrack([])
        return ''.join(result) if result else ""
