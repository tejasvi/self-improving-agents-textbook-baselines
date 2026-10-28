import sys
import math

def main():
    # Read the number of bottles
    N = int(input())
    
    # Calculate minimum number of friends needed (ceil of log2(N))
    M = (N - 1).bit_length()
    
    # Print the number of friends
    print(M)
    sys.stdout.flush()
    
    # Create distribution: for each friend j, determine which bottles to give
    # We use binary representation: bottle i is represented in binary (1-indexed)
    # Friend j gets all bottles where bit j is set to 1 in their binary representation
    
    for friend_idx in range(M):
        bottles = []
        for bottle_num in range(1, N + 1):
            # Check if bit friend_idx is set in bottle_num's binary representation
            if (bottle_num >> friend_idx) & 1:
                bottles.append(bottle_num)
        
        # Print the distribution for this friend
        print(str(len(bottles)) + ' ' + ' '.join(map(str, bottles)))
        sys.stdout.flush()
    
    # Read the feedback from the judge
    S = input().strip()
    
    # Reconstruct the bottle number from the binary pattern
    # The string S gives us the bits directly: S[i] tells us bit i
    spoiled_bottle = 0
    for i in range(M):
        if S[i] == '1':
            spoiled_bottle |= (1 << i)
    
    # Print the answer
    print(spoiled_bottle)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
