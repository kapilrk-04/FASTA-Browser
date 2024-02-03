import threading

total_tasks = 0

# Locks

total_tasks_lock = threading.Lock()
completed_tasks_lock = threading.Lock()

sequence_align_pending_tasks_lock = threading.Lock()
sequence_align_completed_tasks_lock = threading.Lock()

multiple_sequence_align_pending_tasks_lock = threading.Lock()
multiple_sequence_align_completed_tasks_lock = threading.Lock()

phylo_tree_pending_tasks_lock = threading.Lock()
phylo_tree_completed_tasks_lock = threading.Lock()

blast_search_pending_tasks_lock = threading.Lock()
blast_search_completed_tasks_lock = threading.Lock()


