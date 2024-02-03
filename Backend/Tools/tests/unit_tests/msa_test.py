import sys
sys.path.append('../..')
from multiple_sequence_align.multiple_seq_align_module import multiple_seq_aligner

import unittest

class TestMultipleSequenceAlignment(unittest.TestCase):
    
    # use q1seqs.FASTA as sample

    def test_multiple_seq_align(self):
        in_file = 'q1seqs_new.FASTA'
        out_file = 'q1seqs_out.FASTA'
        try:
            multiple_seq_aligner(in_file, out_file)
        except Exception as e:
            print(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()