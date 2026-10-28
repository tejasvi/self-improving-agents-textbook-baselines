class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        word_len = n + m - 1
        
        # Try to build the lexicographically smallest string
        # Using a greedy approach with backtracking
        
        def can_satisfy(word_partial):
            """Check if a partial word can potentially be extended to a valid solution"""
            # For each constraint that can be checked:
            for i in range(len(word_partial) - m + 1):
                if i + m <= len(word_partial):
                    substring = word_partial[i:i+m]
                    if len(substring) == m:
                        if str1[i] == 'T' and substring != str2:
                            return False
                        if str1[i] == 'F' and substring == str2:
                            return False
            return True
        
        def is_valid_complete(word):
            """Check if a complete word is valid"""
            if len(word) != word_len:
                return False
            for i in range(n):
                substring = word[i:i+m]
                if str1[i] == 'T' and substring != str2:
                    return False
                if str1[i] == 'F' and substring == str2:
                    return False
            return True
        
        # Build the word character by character, trying smallest character first
        word = []
        
        def backtrack():
            if len(word) == word_len:
                if is_valid_complete(''.join(word)):
                    return True
                return False
            
            # Try characters from 'a' to 'z'
            for ch in 'abcdefghijklmnopqrstuvwxyz':
                word.append(ch)
                
                if can_satisfy(''.join(word)):
                    if backtrack():
                        return True
                
                word.pop()
            
            return False
        
        if backtrack():
            return ''.join(word)
        return ""
