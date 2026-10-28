class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        word_len = n + m - 1
        
        # Try to build the string greedily
        word = ['a'] * word_len
        
        # First, handle all 'T' constraints - set positions that must match str2
        for i in range(n):
            if str1[i] == 'T':
                # word[i...i+m-1] must equal str2
                for j in range(m):
                    word[i + j] = str2[j]
        
        # Now check if the current word violates any 'F' constraints
        # If it does, try to fix them by incrementing characters
        while True:
            violation_found = False
            
            for i in range(n):
                if str1[i] == 'F':
                    # word[i...i+m-1] must NOT equal str2
                    if ''.join(word[i:i+m]) == str2:
                        # Violation found, try to fix it
                        violation_found = True
                        
                        # Try to increment a character in the substring that doesn't break 'T' constraints
                        # Start from the rightmost position to make lexicographically smallest
                        fixed = False
                        for j in range(m - 1, -1, -1):
                            pos = i + j
                            # Check if this position is constrained by a 'T'
                            can_increment = True
                            
                            # Check all 'T' constraints that affect position pos
                            for t_idx in range(max(0, pos - m + 1), min(n, pos + 1)):
                                if str1[t_idx] == 'T':
                                    # This position must follow str2
                                    if pos < t_idx or pos >= t_idx + m:
                                        continue
                                    # Position pos is constrained by this 'T'
                                    can_increment = False
                                    break
                            
                            if can_increment and word[pos] < 'z':
                                word[pos] = chr(ord(word[pos]) + 1)
                                fixed = True
                                break
                        
                        if not fixed:
                            # Cannot fix this violation
                            return ""
                        
                        break  # Restart checking from the beginning
            
            if not violation_found:
                break
        
        return ''.join(word)
