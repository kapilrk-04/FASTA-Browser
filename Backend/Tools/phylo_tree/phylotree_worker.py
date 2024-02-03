import json
import pika
import sys
sys.path.append('../')
sys.path.append('./phylo_tree')

from phylotree import generate_phylogenetic_tree
from send_email_module import send_mail_with_attachment
from rabbitmq_config import RABBITMQ_CONFIG
from io import StringIO
from Bio import AlignIO, Phylo

import os
import unittest

import common_variables

phylo_channel = None

def process_phylo_tree_task(ch, method, properties, body):
    '''
    worker for phylogenetic tree

    args: .FASTA file with output of multiple sequence alignment
    '''

    try:
        print(" [phylogenetic tree] Received")
        args = json.loads(body.decode('utf-8'))
        print(" [phylogenetic tree] Received arguments")
        align_data = args['align_data']

        with open('temp.fasta', 'w') as f:
            f.write(align_data)
        print(" [phylogenetic tree] Generating phylogenetic tree...")
        temp_out_filename = 'tempout.newick'
        generate_phylogenetic_tree('temp.fasta', temp_out_filename)

        print(" [phylogenetic tree] Done")

        # Read the tree from the output file
        ios = StringIO()
        tree = Phylo.read(temp_out_filename, 'newick')
        tree.rooted = True
        Phylo.draw_ascii(tree, file=ios)
        tree_data = ios.getvalue()

        formatted_str = f"{tree_data}"
        
        print(" [phylogenetic tree] Sending email...")

        send_mail_with_attachment(
            to=args['to'],
            subject='Phylogenetic Tree Result',
            body='<p>Phylogenetic Tree Result</p>',
            attachment_data=bytes(formatted_str, 'utf-8'),
            attachment_name='phylogenetic_tree_result.txt',
            to_mail=args['email'],
        )

        os.remove('tempout.newick')
        ios.close()

        print(" [phylogenetic tree] Email sent")

        print(" [phylogenetic tree] updating pending and completed tasks")

        with common_variables.phylo_tree_pending_tasks_lock:
            with open('phylogeny_pending_tasks.json', 'r') as f:
                pending_tasks = json.load(f)
            if type(pending_tasks) != list:
                with open('phylogeny_pending_tasks.json', 'w') as f:
                    pass
            else:
                pending_tasks = [task for task in pending_tasks if task['task_number'] != args['task_number']]
                with open('phylogeny_pending_tasks.json', 'w') as f:
                    json.dump(pending_tasks, f)

        with common_variables.phylo_tree_completed_tasks_lock:
            with open('phylogeny_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': args['task_number'],
                    'task_name': f'{args["email"]} - {args["task_number"]}',
                    'task_type': 'Phylogenetic Tree',
                    'task_result': 'Success',
                    'mail': args['email'],
                    'status': 'Success',
                }, f)
                f.write('\n')

        print(" [phylogenetic tree] Done")

    except Exception as e:
        print(e)
        print(" [phylogenetic tree] Error")

        print(" [phylogenetic tree] updating pending and completed tasks")
        with common_variables.phylo_tree_pending_tasks_lock:
            with open('phylogeny_pending_tasks.json', 'r') as f:
                pending_tasks = json.load(f)
            if type(pending_tasks) != list:
                with open('phylogeny_pending_tasks.json', 'w') as f:
                    pass
            else:
                pending_tasks = [task for task in pending_tasks if task['task_number'] != args['task_number']]
                with open('phylogeny_pending_tasks.json', 'w') as f:
                    json.dump(pending_tasks, f)

        with common_variables.phylo_tree_completed_tasks_lock:
            with open('phylogeny_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': args['task_number'],
                    'task_name': f'{args["email"]} - {args["task_number"]}',
                    'task_type': 'Phylogenetic Tree',
                    'task_result': 'Failed',
                    'mail': args['email'],
                    'status': 'Failed',
                }, f)
                f.write('\n')

    finally:
        phylo_channel.basic_ack(delivery_tag=method.delivery_tag)
        if os.path.exists('temp.fasta'):
            os.remove('temp.fasta')
        if os.path.exists('tempout.newick'):
            os.remove('tempout.newick')
        if os.path.exists('tempout.png'):
            os.remove('tempout.png')

def start_phylo_tree_worker():
    '''
    start phylogenetic tree worker
    '''
    global phylo_channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_CONFIG['host']))
    phylo_channel = connection.channel()
    phylo_channel.queue_declare(queue='phylo_tree_queue', durable=True)
    phylo_channel.basic_qos(prefetch_count=1)
    phylo_channel.basic_consume(queue='phylo_tree_queue', on_message_callback=process_phylo_tree_task)
    print(' [phylogenetic tree] Waiting for messages. To exit press CTRL+C')
    phylo_channel.start_consuming()


class TestPhylogeneticTreeWithQueue(unittest.TestCase):
    
    def test_phylogenetic_tree(self):
        in_file = 'phylo_tree/multiple_seq_align_resultxx.fasta'
        out_file = 'phylogenetic_tree_result.txt'
        tmp_file = 'tempout.newick'
        try:
            generate_phylogenetic_tree(in_file, tmp_file)
            tree = Phylo.read(tmp_file, 'newick')
            tree.rooted = True
            
            ios = StringIO()
            Phylo.draw_ascii(tree, file=ios)
            out_file = open('ascii_tree.txt', 'w')
            out_file.write(ios.getvalue())
        except Exception as e:
            print(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()