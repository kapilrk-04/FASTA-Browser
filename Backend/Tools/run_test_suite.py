import unittest

import sys
sys.path.append('sequence_align')
sys.path.append('multiple_sequence_align')
sys.path.append('phylo_tree')

from multiple_sequence_align.multiple_seq_align_module import TestMultipleSequenceAlignment
from multiple_sequence_align.multiple_seq_align_worker import TestMultipleSeqAlignWithQueue
from phylo_tree.phylotree import TestPhylogeneticTree
from phylo_tree.phylotree_worker import TestPhylogeneticTreeWithQueue
from sequence_align.seq_align_module import TestSequenceAlignment
from sequence_align.seq_align_worker import TestSequenceAlignWithQueue

if __name__ == '__main__':
    unittest.main()