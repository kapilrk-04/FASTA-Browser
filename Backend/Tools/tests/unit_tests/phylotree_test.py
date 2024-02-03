import sys
sys.path.append('../..')
from phylo_tree.phylotree import generate_phylogenetic_tree
from Bio import Phylo
import io

import unittest

class TestPhylogeneticTree(unittest.TestCase):
    
    def test_phylogenetic_tree(self):
        in_file = 'phylo_tree/multiple_seq_align_resultxx.FASTA'
        out_file = 'phylo_tree/phylogenetic_tree_resultxx.txt'
        tmp_file = 'phylo_tree/tempout.newick'
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