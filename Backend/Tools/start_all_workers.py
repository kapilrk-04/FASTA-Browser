import threading
from sequence_align.seq_align_worker import start_seq_align_worker
from multiple_sequence_align.multiple_seq_align_worker import start_multiple_seq_align_worker
from phylo_tree.phylotree_worker import start_phylo_tree_worker
from blast_search.blast_search_worker import start_blast_search_worker
from common_variables import *

def start_all_workers_in_queue():
    # START MULTIPLE THREADS IN A QUEUE
    thread1 = threading.Thread(target=start_multiple_seq_align_worker)
    thread1.start()

    thread2 = threading.Thread(target=start_seq_align_worker)
    thread2.start()

    thread3 = threading.Thread(target=start_phylo_tree_worker)
    thread3.start()
    
    thread4 = threading.Thread(target=start_blast_search_worker)
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

if __name__ == '__main__':
    start_all_workers_in_queue()