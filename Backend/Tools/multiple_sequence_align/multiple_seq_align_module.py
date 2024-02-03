from Bio import AlignIO
from Bio.Align.Applications import ClustalOmegaCommandline
import unittest
import os

def multiple_seq_aligner(input_fasta, output_fasta):

    '''

    Perform multiple sequence alignment using Clustal Omega
    args:
        input_fasta: .FASTA file with input sequences
        output_fasta: .FASTA file to write the MSA result to
    '''

    # Perform MSA using Clustal Omega
    clustalomega_cline = ClustalOmegaCommandline(infile=input_fasta, outfile=output_fasta, verbose=True, auto=True)
    stdout, stderr = clustalomega_cline()

    # Check for errors in the output
    if stderr:
        print("Error during MSA:", stderr)
    else:
        print("MSA completed successfully.")

class TestMultipleSequenceAlignment(unittest.TestCase):
    
    # use q1seqs.FASTA as sample

    def test_multiple_seq_align(self):
        in_file = "multiple_sequence_align/q1seqs_new.FASTA"
        out_file = 'q1seqs_out.FASTA'
        try:
            multiple_seq_aligner(in_file, out_file)
        except Exception as e:
            print(e)
            self.fail()
        finally:
            os.remove(out_file)

if __name__ == '__main__':
    unittest.main()
        