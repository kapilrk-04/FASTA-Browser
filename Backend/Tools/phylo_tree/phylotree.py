from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import io
import unittest

def generate_phylogenetic_tree(input_aligned_fasta, output_tree_file):

    '''
    Generate a phylogenetic tree using the neighbor-joining method

    args:
            
            input_aligned_fasta: .FASTA file with output of multiple sequence alignment
            output_tree_file: .txt file to write the phylogenetic tree to
    '''
    
    # Read aligned sequences from the input FASTA file
    alignment = AlignIO.read(input_aligned_fasta, "fasta")

    # Calculate the distance matrix
    calculator = DistanceCalculator('identity')
    distance_matrix = calculator.get_distance(alignment)

    # Construct the tree using the neighbor-joining method
    constructor = DistanceTreeConstructor(calculator, 'nj')
    tree = constructor.build_tree(alignment)

    # Save the phylogenetic tree to a Newick format file
    Phylo.write(tree, output_tree_file, 'newick')
    print(f"Phylogenetic tree saved to {output_tree_file}")

class TestPhylogeneticTree(unittest.TestCase):
    
    def test_phylogenetic_tree(self):
        in_file = 'phylo_tree/multiple_seq_align_resultxx.fasta'
        out_file = 'phylogenetic_tree_result.txt'
        tmp_file = 'tempout.newick'
        try:
            generate_phylogenetic_tree(in_file, tmp_file)
            tree = Phylo.read(tmp_file, 'newick')
            tree.rooted = True
            
            ios = io.StringIO()
            Phylo.draw_ascii(tree, file=ios)
            out_file = open('ascii_tree.txt', 'w')
            out_file.write(ios.getvalue())
        except Exception as e:
            print(e)
            self.fail()


if __name__ == '__main__':
    unittest.main()


