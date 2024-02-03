import unittest

# Use these values to calculate scores
gap_penalty = -1
match_award = 1
mismatch_penalty = -1

A="A"
T="T"
G="G"
C="C"
S="S"
W="W"
R="R"
Y="Y"
K="K"
M="M"
B="B"
V="V"
H="H"
D="D"
N="N"

DNAfull = {
    (A, A): 5, (A, T): -4, (A, G): -4, (A, C): -4, (A, S): -4, (A, W): 1, (A, R): 1, (A, Y): -4, (A, K): -4, (A, M): 1, (A, B): -4, (A, V): -1, (A, H): -1, (A, D): -1, (A, N): -2,
    (T, A): -4, (T, T): 5, (T, G): -4, (T, C): -4, (T, S): -4, (T, W): 1, (T, R): -4, (T, Y): 1, (T, K): 1, (T, M): -4, (T, B): -1, (T, V): -4, (T, H): -1, (T, D): -1, (T, N): -2,
    (G, A): -4, (G, T): -4, (G, G): 5, (G, C): -4, (G, S): 1, (G, W): -4, (G, R): 1, (G, Y): -4, (G, K): 1, (G, M): -4, (G, B): -1, (G, V): -1, (G, H): -4, (G, D): -1, (G, N): -2,
    (C, A): -4, (C, T): -4, (C, G): -4, (C, C): 5, (C, S): 1, (C, W): -4, (C, R): -4, (C, Y): 1, (C, K): -4, (C, M): 1, (C, B): -1, (C, V): -1, (C, H): -1, (C, D): -4, (C, N): -2,
    (S, A): -4, (S, T): -4, (S, G): 1, (S, C): 1, (S, S): -1, (S, W): -4, (S, R): -2, (S, Y): -2, (S, K): -2, (S, M): -2, (S, B): -1, (S, V): -1, (S, H): -3, (S, D): -3, (S, N): -1,
    (W, A): 1, (W, T): 1, (W, G): -4, (W, C): -4, (W, S): -4, (W, W): -1, (W, R): -2, (W, Y): -2, (W, K): -2, (W, M): -2, (W, B): -3, (W, V): -3, (W, H): -1, (W, D): -1, (W, N): -1,
    (R, A): 1, (R, T): -4, (R, G): 1, (R, C): -4, (R, S): -2, (R, W): -2, (R, R): -1, (R, Y): -4, (R, K): -2, (R, M): -2, (R, B): -3, (R, V): -1, (R, H): -3, (R, D): -1, (R, N): -1,
    (Y, A): -4, (Y, T): 1, (Y, G): -4, (Y, C): 1, (Y, S): -2, (Y, W): -2, (Y, R): -4, (Y, Y): -1, (Y, K): -2, (Y, M): -2, (Y, B): -1, (Y, V): -3, (Y, H): -1, (Y, D): -3, (Y, N): -1,
    (K, A): -4, (K, T): 1, (K, G): 1, (K, C): -4, (K, S): -2, (K, W): -2, (K, R): -2, (K, Y): -2, (K, K): -1, (K, M): -4, (K, B): -1, (K, V): -3, (K, H): -3, (K, D): -1, (K, N): -1,
    (M, A): 1, (M, T): -4, (M, G): -4, (M, C): 1, (M, S): -2, (M, W): -2, (M, R): -2, (M, Y): -2, (M, K): -4, (M, M): -1, (M, B): -3, (M, V): -1, (M, H): -1, (M, D): -3, (M, N): -1,
    (B, A): -4, (B, T): -1, (B, G): -1, (B, C): -1, (B, S): -1, (B, W): -3, (B, R): -3, (B, Y): -1, (B, K): -1, (B, M): -3, (B, B): -1, (B, V): -2, (B, H): -2, (B, D): -2, (B, N): -1,
    (V, A): -1, (V, T): -4, (V, G): -1, (V, C): -1, (V, S): -1, (V, W): -3, (V, R): -1, (V, Y): -3,  (V, K): -3, (V, M): -1, (V, B): -2, (V, V): -1, (V, H): -2, (V, D): -2, (V, N): -1,
    (H, A): -1, (H, T): -1, (H, G): -4, (H, C): -1, (H, S): -3, (H, W): -1, (H, R): -3, (H, Y): -1, (H, K): -3, (H, M): -1, (H, B): -2, (H, V): -2, (H, H): -1, (H, D): -2, (H, N): -1,
    (D, A): -1, (D, T): -1, (D, G): -1, (D, C): -4, (D, S): -3, (D, W): -1, (D, R): -1, (D, Y): -3, (D, K): -1, (D, M): -3, (D, B): -2, (D, V): -2, (D, H): -2, (D, D): -1, (D, N): -1,
    (N, A): -2, (N, T): -2, (N, G): -2, (N, C): -2, (N, S): -1, (N, W): -1, (N, R): -1, (N, Y): -1, (N, K): -1, (N, M): -1, (N, B): -1, (N, V): -1, (N, H): -1, (N, D): -1, (N, N): -1
}

blosum62 = {
    ('W', 'F'): 1, ('L', 'R'): -2, ('S', 'P'): -1, ('V', 'T'): 0,
    ('Q', 'Q'): 5, ('N', 'A'): -2, ('Z', 'Y'): -2, ('W', 'R'): -3,
    ('Q', 'A'): -1, ('S', 'D'): 0, ('H', 'H'): 8, ('S', 'H'): -1,
    ('H', 'D'): -1, ('L', 'N'): -3, ('W', 'A'): -3, ('Y', 'M'): -1,
    ('G', 'R'): -2, ('Y', 'I'): -1, ('Y', 'E'): -2, ('B', 'Y'): -3,
    ('Y', 'A'): -2, ('V', 'D'): -3, ('B', 'S'): 0, ('Y', 'Y'): 7,
    ('G', 'N'): 0, ('E', 'C'): -4, ('Y', 'Q'): -1, ('Z', 'Z'): 4,
    ('V', 'A'): 0, ('C', 'C'): 9, ('M', 'R'): -1, ('V', 'E'): -2,
    ('T', 'N'): 0, ('P', 'P'): 7, ('V', 'I'): 3, ('V', 'S'): -2,
    ('Z', 'P'): -1, ('V', 'M'): 1, ('T', 'F'): -2, ('V', 'Q'): -2,
    ('K', 'K'): 5, ('P', 'D'): -1, ('I', 'H'): -3, ('I', 'D'): -3,
    ('T', 'R'): -1, ('P', 'L'): -3, ('K', 'G'): -2, ('M', 'N'): -2,
    ('P', 'H'): -2, ('F', 'Q'): -3, ('Z', 'G'): -2, ('X', 'L'): -1,
    ('T', 'M'): -1, ('Z', 'C'): -3, ('X', 'H'): -1, ('D', 'R'): -2,
    ('B', 'W'): -4, ('X', 'D'): -1, ('Z', 'K'): 1, ('F', 'A'): -2,
    ('Z', 'W'): -3, ('F', 'E'): -3, ('D', 'N'): 1, ('B', 'K'): 0,
    ('X', 'X'): -1, ('F', 'I'): 0, ('B', 'G'): -1, ('X', 'T'): 0,
    ('F', 'M'): 0, ('B', 'C'): -3, ('Z', 'I'): -3, ('Z', 'V'): -2,
    ('S', 'S'): 4, ('L', 'Q'): -2, ('W', 'E'): -3, ('Q', 'R'): 1,
    ('N', 'N'): 6, ('W', 'M'): -1, ('Q', 'C'): -3, ('W', 'I'): -3,
    ('S', 'C'): -1, ('L', 'A'): -1, ('S', 'G'): 0, ('L', 'E'): -3,
    ('W', 'Q'): -2, ('H', 'G'): -2, ('S', 'K'): 0, ('Q', 'N'): 0,
    ('N', 'R'): 0, ('H', 'C'): -3, ('Y', 'N'): -2, ('G', 'Q'): -2,
    ('Y', 'F'): 3, ('C', 'A'): 0, ('V', 'L'): 1, ('G', 'E'): -2,
    ('G', 'A'): 0, ('K', 'R'): 2, ('E', 'D'): 2, ('Y', 'R'): -2,
    ('M', 'Q'): 0, ('T', 'I'): -1, ('C', 'D'): -3, ('V', 'F'): -1,
    ('T', 'A'): 0, ('T', 'P'): -1, ('B', 'P'): -2, ('T', 'E'): -1,
    ('V', 'N'): -3, ('P', 'G'): -2, ('M', 'A'): -1, ('K', 'H'): -1,
    ('V', 'R'): -3, ('P', 'C'): -3, ('M', 'E'): -2, ('K', 'L'): -2,
    ('V', 'V'): 4, ('M', 'I'): 1, ('T', 'Q'): -1, ('I', 'G'): -4,
    ('P', 'K'): -1, ('M', 'M'): 5, ('K', 'D'): -1, ('I', 'C'): -1,
    ('Z', 'D'): 1, ('F', 'R'): -3, ('X', 'K'): -1, ('Q', 'D'): 0,
    ('X', 'G'): -1, ('Z', 'L'): -3, ('X', 'C'): -2, ('Z', 'H'): 0,
    ('B', 'L'): -4, ('B', 'H'): 0, ('F', 'F'): 6, ('X', 'W'): -2,
    ('B', 'D'): 4, ('D', 'A'): -2, ('S', 'L'): -2, ('X', 'S'): 0,
    ('F', 'N'): -3, ('S', 'R'): -1, ('W', 'D'): -4, ('V', 'Y'): -1,
    ('W', 'L'): -2, ('H', 'R'): 0, ('W', 'H'): -2, ('H', 'N'): 1,
    ('W', 'T'): -2, ('T', 'T'): 5, ('S', 'F'): -2, ('W', 'P'): -4,
    ('L', 'D'): -4, ('B', 'I'): -3, ('L', 'H'): -3, ('S', 'N'): 1,
    ('B', 'T'): -1, ('L', 'L'): 4, ('Y', 'K'): -2, ('E', 'Q'): 2,
    ('Y', 'G'): -3, ('Z', 'S'): 0, ('Y', 'C'): -2, ('G', 'D'): -1,
    ('B', 'V'): -3, ('E', 'A'): -1, ('Y', 'W'): 2, ('E', 'E'): 5,
    ('Y', 'S'): -2, ('C', 'N'): -3, ('V', 'C'): -1, ('T', 'H'): -2,
    ('P', 'R'): -2, ('V', 'G'): -3, ('T', 'L'): -1, ('V', 'K'): -2,
    ('K', 'Q'): 1, ('R', 'A'): -1, ('I', 'R'): -3, ('T', 'D'): -1,
    ('P', 'F'): -4, ('I', 'N'): -3, ('K', 'I'): -3, ('M', 'D'): -3,
    ('V', 'W'): -3, ('W', 'W'): 11, ('M', 'H'): -2, ('P', 'N'): -2,
    ('K', 'A'): -1, ('M', 'L'): 2, ('K', 'E'): 1, ('Z', 'E'): 4,
    ('X', 'N'): -1, ('Z', 'A'): -1, ('Z', 'M'): -1, ('X', 'F'): -1,
    ('K', 'C'): -3, ('B', 'Q'): 0, ('X', 'B'): -1, ('B', 'M'): -3,
    ('F', 'C'): -2, ('Z', 'Q'): 3, ('X', 'Z'): -1, ('F', 'G'): -3,
    ('B', 'E'): 1, ('X', 'V'): -1, ('F', 'K'): -3, ('B', 'A'): -2,
    ('X', 'R'): -1, ('D', 'D'): 6, ('W', 'G'): -2, ('Z', 'F'): -3,
    ('S', 'Q'): 0, ('W', 'C'): -2, ('W', 'K'): -3, ('H', 'Q'): 0,
    ('L', 'C'): -1, ('W', 'N'): -4, ('S', 'A'): 1, ('L', 'G'): -4,
    ('W', 'S'): -3, ('S', 'E'): 0, ('H', 'E'): 0, ('S', 'I'): -2,
    ('H', 'A'): -2, ('S', 'M'): -1, ('Y', 'L'): -1, ('Y', 'H'): 2,
    ('Y', 'D'): -3, ('E', 'R'): 0, ('X', 'P'): -2, ('G', 'G'): 6,
    ('G', 'C'): -3, ('E', 'N'): 0, ('Y', 'T'): -2, ('Y', 'P'): -3,
    ('T', 'K'): -1, ('A', 'A'): 4, ('P', 'Q'): -1, ('T', 'C'): -1,
    ('V', 'H'): -3, ('T', 'G'): -2, ('I', 'Q'): -3, ('Z', 'T'): -1,
    ('C', 'R'): -3, ('V', 'P'): -2, ('P', 'E'): -1, ('M', 'C'): -1,
    ('K', 'N'): 0, ('I', 'I'): 4, ('P', 'A'): -1, ('M', 'G'): -3,
    ('T', 'S'): 1, ('I', 'E'): -3, ('P', 'M'): -2, ('M', 'K'): -1,
    ('I', 'A'): -1, ('P', 'I'): -3, ('R', 'R'): 5, ('X', 'M'): -1,
    ('L', 'I'): 2, ('X', 'I'): -1, ('Z', 'B'): 1, ('X', 'E'): -1,
    ('Z', 'N'): 0, ('X', 'A'): 0, ('B', 'R'): -1, ('B', 'N'): 3,
    ('F', 'D'): -3, ('X', 'Y'): -1, ('Z', 'R'): 0, ('F', 'H'): -1,
    ('B', 'F'): -3, ('F', 'L'): 0, ('X', 'Q'): -1, ('B', 'B'): 4
}

# A function for making a matrix of zeroes
def zeros(rows, cols):
    # Define an empty list
    retval = []
    # Set up the rows of the matrix
    for x in range(rows):
        # For each row, add an empty list
        retval.append([])
        # Set up the columns in each row
        for y in range(cols):
            # Add a zero to each column in each row
            retval[-1].append(0)
    # Return the matrix of zeros
    return retval

# A function for determining the score between any two bases in alignment
def match_score(alpha, beta, matrix):
    if (alpha, beta) in matrix.keys():
        return matrix[(alpha, beta)]
    else:
        return matrix[(beta, alpha)]

# The function that actually fills out a matrix of scores
def needleman_wunsch(seq1, seq2, matrix):
    print(seq1, seq2)
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = zeros(m+1, n+1)
   
    # Calculate score table
    
    # Fill out first column
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    # Fill out first row
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1], matrix)
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    
    # Create variables to store alignment
    align1 = ""
    align2 = ""
    
    # Start from the bottom right cell in matrix
    i = m
    j = n
    
    # We'll use i and j to keep track of where we are in the matrix, just like above
    while i > 0 and j > 0: # end touching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1], matrix):
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += seq1[j-1]
            align2 += '-'
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += '-'
            align2 += seq2[i-1]
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    align1 = align1[::-1]
    align2 = align2[::-1]
    print(align1, align2)
    return(align1, align2)


def smith_waterman(seq1, seq2, matrix):
    print(seq1, seq2)
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = zeros(m+1, n+1)
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1], matrix)
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert, 0)
    

    align1 = ""
    align2 = ""
    
    i = m
    j = n
    
    while i > 0 and j > 0:
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]

        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1], matrix):
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += seq1[j-1]
            align2 += '-'
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += '-'
            align2 += seq2[i-1]
            i -= 1

    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        i -= 1

    align1 = align1[::-1]
    align2 = align2[::-1]
    print(align1, align2)
    return(align1, align2)


def seq_alignment(algo, seq1, seq2, matrix):

    '''
    Perform sequence alignment

    args:
        Algo: algorithm to use
        seq1: sequence 1
        seq2: sequence 2
        matrix: matrix to use

    '''

    print(seq1, seq2)
    seq1 = seq1.replace("\r", "")
    seq2 = seq2.replace("\r", "")
    seq1 = seq1.split("\n")[1:]
    seq2 = seq2.split("\n")[1:]
    for i in range(len(seq1)):
        seq1[i] = seq1[i].strip()
    for i in range(len(seq2)):
        seq2[i] = seq2[i].strip()
    seq1 = "".join(seq1)
    seq2 = "".join(seq2)
    print(seq1, seq2)
    print("Aligning sequences...")
    if algo == "needleman_wunsch":
        return needleman_wunsch(seq1, seq2, matrix)
    elif algo == "smith_waterman":
        return smith_waterman(seq1, seq2, matrix)
    print("Done")
    
class TestSequenceAlignment(unittest.TestCase):
    def test_seq_align(self):
        try:
            args = {
                'algo': 'needleman_wunsch',
                'seq1': '>seq1\nATCG',
                'seq2': '>seq2\nATCG',
                'matrix': 'blosum62',
            }
            (sq1, sq2) = seq_alignment(args['algo'], args['seq1'], args['seq2'], blosum62)
            self.assertEqual(sq1, 'ATCG')
            self.assertEqual(sq2, 'ATCG')
        except Exception as e:
            print(e)
            self.fail()

    def test_seq_align2(self):
        try:
            args = {
                'algo': 'smith_waterman',
                'seq1': '>seq1\nATCG',
                'seq2': '>seq1\nATCG',
                'matrix': 'DNAfull',
            }
            (sq1, sq2) = seq_alignment(args['algo'], args['seq1'], args['seq2'], DNAfull)
            self.assertEqual(sq1, 'ATCG')
            self.assertEqual(sq2, 'ATCG')
        except Exception as e:
            print(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()