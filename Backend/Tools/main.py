from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import pika
import json
from rabbitmq_config import RABBITMQ_CONFIG

from variation_analyzer.va_module import get_valid_parts_fromdb
import asyncio

import common_variables

task_cnt = 0

# Allow CORS
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


'''
    Pairwise Sequence Alignment

    args: {
        'algo': algorithm,
        'seq1': sequence1,
        'seq2': sequence2,
        'matrix': matrix,
        'to': [mail],
        'to_mail': mail,
        'task_number': task_cnt,
    }
'''

class SeqAlignRequest(BaseModel):
    algo: str
    seq1: str
    seq2: str
    matrix: str
    mail: str

class SeqAlignResponse(BaseModel):
    seq1: list
    seq2: list
    matches: list
    per_line_out: str

@app.post("/seq_align")
async def seq_align(request: SeqAlignRequest):

    seq1 = request.seq1
    seq2 = request.seq2
    matrix = request.matrix
    algo = request.algo
    mail = request.mail

    try:
        with open('sequence_align_pending_tasks.json', 'r') as f:
            pending_tasks = json.loads(f.read())
    except (json.JSONDecodeError, FileNotFoundError):
        pending_tasks = []
    print(pending_tasks)
    if type(pending_tasks) == list:
        task_user_cnt = len([task for task in pending_tasks if task['mail'] == mail])
        if task_user_cnt >= 3:
            raise Exception('You can only have 3 pending tasks at the same time.')

    if mail == '' or mail == None:
        raise Exception('Please input your email address.')
    
    if algo == '' or algo == None:
        raise Exception('Please input the algorithm to use.')
    
    if seq1 == '' or seq1 == None:
        raise Exception('Please input the first sequence.')
    
    if seq2 == '' or seq2 == None:
        raise Exception('Please input the second sequence.')
    
    if matrix == '' or matrix == None:
        raise Exception('Please input the matrix to use.')
    
    with common_variables.total_tasks_lock:
        global task_cnt
        task_cnt += 1
    
    with common_variables.sequence_align_pending_tasks_lock:

        with open('sequence_align_pending_tasks.json', 'a') as f:
            json.dump({
                'task_number': task_cnt,
                'task_name': f'{mail} - {task_cnt}',
                'task_type': 'Pairwise Sequence Alignment',
                'task_result': 'Pending',
                'mail': mail,
                'status': 'Pending',
            }, f)
            f.write('\n')

    args = {
        'algo': algo,
        'seq1': seq1,
        'seq2': seq2,
        'matrix': matrix,
        'to': [mail],
        'to_mail': mail,
        'task_number': task_cnt,
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        heartbeat=0, blocked_connection_timeout=0,
        host=RABBITMQ_CONFIG['host'], 
        port=RABBITMQ_CONFIG['port'],
        credentials=pika.PlainCredentials(RABBITMQ_CONFIG['username'], RABBITMQ_CONFIG['password'])))
    channel = connection.channel()
    channel.confirm_delivery()
    channel.queue_declare(queue=RABBITMQ_CONFIG['seq_align_queue'], durable=True)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_CONFIG['seq_align_queue'], body=json.dumps(args), properties=pika.BasicProperties(delivery_mode=2))
    print(" [sequence aligner] Sent 'Hello World!'")

    # add to pending tasks
    connection.close()
    print(f" [sequence aligner] Task {common_variables.total_tasks} added to pending tasks")



'''
    Multiple Sequence Alignment
'''

class MultiSeqAlignRequest(BaseModel):
    seqs: str
    genTree: bool
    mail: str

class MultiSeqAlignResponse(BaseModel):
    seqs: list
    matches: list
    per_line_out: str

@app.post("/multi_seq_align")
async def multi_seq_align(request: MultiSeqAlignRequest):
    # print(request)
    seqs = request.seqs
    gentree = request.genTree
    mail = request.mail

    try:
        with open('msa_pending_tasks.json', 'r') as f:
            pending_tasks = json.loads(f.read())
    except (json.JSONDecodeError, FileNotFoundError):
        pending_tasks = []
    if type(pending_tasks) == list:
        task_user_cnt = len([task for task in pending_tasks if task['mail'] == mail])
        if task_user_cnt >= 3:
            raise Exception('You can only have 3 pending tasks at the same time.')

    if mail == '' or mail == None:
        raise Exception('Please input your email address.')
    
    if seqs == '' or seqs == None:
        raise Exception('Please input the sequences.')

    with common_variables.total_tasks_lock:
        global task_cnt
        task_cnt += 1

    with common_variables.multiple_sequence_align_pending_tasks_lock:
           
        with open('msa_pending_tasks.json', 'a') as f:
            json.dump({
                'task_number': task_cnt,
                'task_name': f'{mail} - {task_cnt}',
                'task_type': 'Multiple Sequence Alignment',
                'task_result': 'Pending',
                'mail': mail,
                'status': 'Pending',
            }, f)
            f.write('\n')

    args = {
        'align_data': seqs,
        'generate_tree': gentree,
        'to': [mail],
        'email': mail,
        'task_number': task_cnt,
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        heartbeat=0, blocked_connection_timeout=0,
        host=RABBITMQ_CONFIG['host'], 
        port=RABBITMQ_CONFIG['port'],
        credentials=pika.PlainCredentials(RABBITMQ_CONFIG['username'], RABBITMQ_CONFIG['password'])))
    
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_CONFIG['multiple_seq_align_queue'], durable=True)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_CONFIG['multiple_seq_align_queue'], body=json.dumps(args), properties=pika.BasicProperties(delivery_mode=2))
    print(" [multiple sequence aligner] Sent 'Hello World!'")

    connection.close()

'''
    Phylogenetic Tree
'''

class PhyloTreeRequest(BaseModel):
    seqs: str
    mail: str

class PhyloTreeResponse(BaseModel):
    tree: str

@app.post("/phylo_tree")
async def phylo_tree(request: PhyloTreeRequest):
    # print(request)
    seqs = request.seqs
    mail = request.mail

    try:
        with open('phylogeny_pending_tasks.json', 'r') as f:
            pending_tasks = json.loads(f.read())
    except (json.JSONDecodeError, FileNotFoundError):
        pending_tasks = []
    if type(pending_tasks) == list:
        task_user_cnt = len([task for task in pending_tasks if task['mail'] == mail])
        if task_user_cnt >= 3:
            raise Exception('You can only have 3 pending tasks at the same time.')


    if mail == '' or mail == None:
        raise Exception('Please input your email address.')
    
    if seqs == '' or seqs == None:
        raise Exception('Please input the sequences.')
    
    with common_variables.total_tasks_lock:
        global task_cnt
        task_cnt += 1

    with common_variables.phylo_tree_pending_tasks_lock:
           
        with open('phylogeny_pending_tasks.json', 'a') as f:
            json.dump({
                'task_number': task_cnt,
                'task_name': f'{mail} - {task_cnt}',
                'task_type': 'Phylogenetic Tree',
                'task_result': 'Pending',
                'mail': mail,
                'status': 'Pending',
            }, f)
            f.write('\n')

    args = {
        'align_data': seqs,
        'to': [mail],
        'email': mail,
        'task_number': task_cnt,
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_CONFIG['host'], blocked_connection_timeout=0))
    phylo_channel = connection.channel()
    phylo_channel.queue_declare(queue='phylo_tree_queue', durable=True)
    phylo_channel.basic_publish(exchange='', routing_key='phylo_tree_queue', body=json.dumps(args), properties=pika.BasicProperties(delivery_mode=2))
    print(" [phylogenetic tree] Sent 'Hello World!'")

    connection.close()

'''
    BLAST Search
'''

class BlastSearchRequest(BaseModel):
    fasta_file: str
    blast_program: str
    database: str
    num_alignments: int
    mail: str

class BlastSearchResponse(BaseModel):
    blast_out: str

@app.post("/blast_search")
async def blast_search(request: BlastSearchRequest):
    print(request)
    fasta_file = request.fasta_file
    blast_program = request.blast_program
    database = request.database
    num_alignments = request.num_alignments
    mail = request.mail

    print("check validity of inputs and req")
    try:
        with open('blast_pending_tasks.json', 'r') as f:
            pending_tasks = json.loads(f.read())
            print(pending_tasks)
    except json.JSONDecodeError:
        print("error json decode")
        pending_tasks = []
    except FileNotFoundError:
        print("error file not found")
        pending_tasks = []
    print(pending_tasks)
    if type(pending_tasks) == list:
        task_user_cnt = len([task for task in pending_tasks if task['mail'] == mail])
        print(task_user_cnt)
        if task_user_cnt >= 3:
            raise Exception('You can only have 3 pending tasks at the same time.')

    if mail == '' or mail == None:
        raise Exception('Please input your email address.')
    
    if fasta_file == '' or fasta_file == None:
        raise Exception('Please input the fasta file.')
    
    if blast_program == '' or blast_program == None:
        raise Exception('Please input the blast program.')
    
    if database == '' or database == None:
        raise Exception('Please input the database.')
    
    if num_alignments == '' or num_alignments == None:
        raise Exception('Please input the number of alignments.')
    
    with common_variables.total_tasks_lock:
        global task_cnt
        task_cnt += 1

    with common_variables.blast_search_pending_tasks_lock:
        with open('blast_pending_tasks.json', 'a') as f:
            json.dump({
                'task_number': task_cnt,
                'task_name': f'{mail} - {task_cnt}',
                'task_type': 'BLAST Search',
                'task_result': 'Pending',
                'mail': mail,
                'status': 'Pending',
            }, f)
            f.write('\n')

    args = {
        'fasta_file': fasta_file,
        'blast_program': blast_program,
        'database': database,
        'num_alignments': num_alignments,
        'to': [mail],
        'email': mail,
        'task_number': task_cnt,
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_CONFIG['host'], blocked_connection_timeout=0))
    blast_channel = connection.channel()
    blast_channel.queue_declare(queue='blast_search_queue', durable=True)
    blast_channel.basic_publish(exchange='', routing_key='blast_search_queue', body=json.dumps(args), properties=pika.BasicProperties(delivery_mode=2))
    print(" [BLAST search] Sent 'Hello World!'")

    connection.close()


'''
    Variation Analyzer
'''

@app.get("/get_valid_parts")
async def get_valid_parts():
    valid_parts, valid_parts_files = await get_valid_parts_fromdb()
    print(valid_parts)
    #print(valid_parts_files)
    print(type(valid_parts))
    print(type(valid_parts_files))
    return {
        'valid_parts': valid_parts,
        'valid_parts_files': valid_parts_files
    }


'''
    Get info from all RabbitMQ queues
'''
@app.get("/get_queue_info")
async def get_queue_info():
    seq_align_pending_tasks = []
    with open('sequence_align_pending_tasks.json', 'r') as f:
         for line in f.readlines():
              seq_align_pending_tasks.append(json.loads(line))

    seq_align_completed_tasks = []
    with open('sequence_align_completed_tasks.json', 'r') as f:
         for line in f.readlines():
              seq_align_completed_tasks.append(json.loads(line))

    multiple_seq_align_pending_tasks = []
    with open('msa_pending_tasks.json', 'r') as f:
         for line in f.readlines():
              multiple_seq_align_pending_tasks.append(json.loads(line))

    multiple_seq_align_completed_tasks = []
    with open('msa_completed_tasks.json', 'r') as f:
         for line in f.readlines():
              multiple_seq_align_completed_tasks.append(json.loads(line))

    phylo_tree_pending_tasks = []
    with open('phylogeny_pending_tasks.json', 'r') as f:
         for line in f.readlines():
              phylo_tree_pending_tasks.append(json.loads(line))

    phylo_tree_completed_tasks = []
    with open('phylogeny_completed_tasks.json', 'r') as f:
         for line in f.readlines():
              phylo_tree_completed_tasks.append(json.loads(line))

    blast_search_pending_tasks = []
    with open('blast_pending_tasks.json', 'r') as f:
         for line in f.readlines():
              blast_search_pending_tasks.append(json.loads(line))

    blast_search_completed_tasks = []
    with open('blast_completed_tasks.json', 'r') as f:
         for line in f.readlines():
              blast_search_completed_tasks.append(json.loads(line))

    print(seq_align_pending_tasks)
    print(seq_align_completed_tasks)
    print(multiple_seq_align_pending_tasks)
    print(multiple_seq_align_completed_tasks)
    print(phylo_tree_pending_tasks)
    print(phylo_tree_completed_tasks)
    print(blast_search_pending_tasks)
    print(blast_search_completed_tasks)

    return {
        'seq_align_pending_tasks': seq_align_pending_tasks,
        'seq_align_completed_tasks': seq_align_completed_tasks,
        'multiple_seq_align_pending_tasks': multiple_seq_align_pending_tasks,
        'multiple_seq_align_completed_tasks': multiple_seq_align_completed_tasks,
        'phylo_tree_pending_tasks': phylo_tree_pending_tasks,
        'phylo_tree_completed_tasks': phylo_tree_completed_tasks,
        'blast_search_pending_tasks': blast_search_pending_tasks,
        'blast_search_completed_tasks': blast_search_completed_tasks,
    }
   