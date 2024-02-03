import sys
sys.path.append('../..')
from sequence_align.seq_align_module import seq_alignment, blosum62, DNAfull

import unittest

class TestSequenceAlignment(unittest.TestCase):
    def test_seq_align(self):
        try:
            args = {
                'algo': 'global',
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
                'algo': 'global',
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


