class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        word_len = n + m - 1
        
        # Start with all 'a's
        word = ['a'] * word_len
        
        # First pass: apply all 'T' constraints
        for i in range(n):
            if str1[i] == 'T':
                # word[i:i+m] must equal str2
                for j in range(m):
                    word[i + j] = str2[j]
        
        # Check if all 'T' constraints are consistent
        # (this is implicit in the loop above, but we need to validate later)
        
        # Second pass: validate and adjust for 'F' constraints
        for i in range(n):
            if str1[i] == 'F':
                # word[i:i+m] must NOT equal str2
                substring = ''.join(word[i:i+m])
                if substring == str2:
                    # Try to change one character to make it different
                    # We want the lexicographically smallest change
                    changed = False
                    for j in range(m):
                        # Try to increment character at position i+j
                        if word[i + j] < 'z':
                            original = word[i + j]
                            word[i + j] = chr(ord(word[i + j]) + 1)
                            substring = ''.join(word[i:i+m])
                            if substring != str2:
                                changed = True
                                break
                            else:
                                word[i + j] = original
                    
                    if not changed:
                        # Could not fix this constraint
                        return ""
        
        # Verify all constraints
        for i in range(n):
            substring = ''.join(word[i:i+m])
            if str1[i] == 'T':
                if substring != str2:
                    return ""
            else:  # str1[i] == 'F'
                if substring == str2:
                    return ""
        
        return ''.join(word)
