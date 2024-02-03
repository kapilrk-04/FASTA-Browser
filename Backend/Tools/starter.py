from start_all_workers import start_all_workers_in_queue
from common_variables import *
import json

if __name__ == '__main__':
    for name in ['sequence_align', 'msa', 'phylogeny', 'blast']:
        for status in ['pending', 'completed']:
            with open(f'{name}_{status}_tasks.json', 'w') as f:
                pass
    start_all_workers_in_queue()