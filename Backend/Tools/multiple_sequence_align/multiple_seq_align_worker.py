import json
import pika
import sys
sys.path.append('../')
sys.path.append('./multiple_sequence_align')
from multiple_seq_align_module import multiple_seq_aligner
from phylo_tree.phylotree import generate_phylogenetic_tree
from io import StringIO
from Bio import AlignIO, Phylo

from send_email_module import send_mail_with_attachment
from pymsaviz import MsaViz
from rabbitmq_config import RABBITMQ_CONFIG
import os
import unittest

import common_variables

written = False

msa_channel = None

def process_multiple_seq_align_task(ch, method, properties, body):

    '''
    worker for multiple sequence alignment

    args:

        body: {
            'align_data': align_data,
            'generate_tree': generate_tree,
            'to': [mail],
            'email': email,
            'task_number': task_number,
        }
    '''

    try:
        # get arguments
        global written
        written = False
        print(" [multiple sequence aligner] Received")
        args = json.loads(body.decode('utf-8'))
        print(" [multiple sequence aligner] Received arguments")
        align_data = args['align_data']

        # write arguments to a temporary file which will be used by the multiple sequence aligner
        with open('temp.fasta', 'w') as f:
            f.write(align_data)

        # define a temporary output file which will be used by the multiple sequence aligner, then call the multiple sequence aligner
        print(" [multiple sequence aligner] Aligning...")
        temp_out_filename = 'tempout.fasta'
        multiple_seq_aligner('temp.fasta', temp_out_filename)

        # use the output file to generate a color coded alignment image
        mv = MsaViz(temp_out_filename, wrap_length=50, show_count=True)
        mv.savefig('tempout.png')

        # read the output file and send it as an email attachment
        with open(temp_out_filename, 'r') as f:
            out_data = f.read()        

        print(" [multiple sequence aligner] Done")

        email_result = {
            'align_data': align_data,
            'out_data': out_data
        }

        # format the output string
        formatted_str = f"{email_result['out_data']}"

        # if tree generation is requested, generate the tree and send it as an email attachment
        if args['generate_tree']:
            print(" [multiple sequence aligner] Generating phylogenetic tree...")
            temp_out_filename = 'tempout.newick'
            generate_phylogenetic_tree('tempout.fasta', temp_out_filename)
            ios = StringIO()
            tree = Phylo.read(temp_out_filename, 'newick')
            tree.rooted = True
            Phylo.draw_ascii(tree, file=ios)
            tree_data = ios.getvalue()
            formatted_tree = f"{tree_data}"
        
        print(" [multiple sequence aligner] Sending email...")

        task_num = args['task_number']
        print(f" [multiple sequence aligner] Task number: {task_num}")

        # send the email
        send_mail_with_attachment(
            to=args['to'], 
            subject=f"Multiple Sequence Alignment - {task_num}",
            body=formatted_str,
            attachment_data=out_data,
            attachment_name='alignment.fasta',
            to_mail=args['email'],
            program='msa',
            imgpath='tempout.png',
            tree_attachment=formatted_tree if args['generate_tree'] else None,
        )

        # remove the temporary files
        os.remove('temp.fasta')
        os.remove('tempout.fasta')
        os.remove('tempout.png')
        if args['generate_tree']:
            os.remove('tempout.newick')

        print(" [multiple sequence aligner] Email sent")

        # update pending tasks and completed tasks
        print(f" [multiple sequence aligner] Updating pending and completed tasks...")

        with common_variables.multiple_sequence_align_pending_tasks_lock:
            with open('msa_pending_tasks.json', 'r') as f:
                tasks = json.load(f)
            print(f" [multiple sequence aligner] Pending tasks: {tasks}")
            print(type(tasks))
            if type(tasks) != list:
                with open('msa_pending_tasks.json', 'w') as f:
                    pass
            else:
                print(f" [multiple sequence aligner] Pending tasks: {tasks}")
                tasks = [task for task in tasks if task['task_number'] != task_num]
                with open('msa_pending_tasks.json', 'w') as f:
                    json.dump(tasks, f)

        with common_variables.multiple_sequence_align_completed_tasks_lock:
            with open('msa_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': task_num,
                    'task_name': f'{args["email"]} - {task_num}',
                    'task_type': 'Multiple Sequence Alignment',
                    'task_result': 'Success',
                    'mail': args['email'],
                    'status': 'Success',
                }, f)
                f.write('\n')

        written = True

        print(f" [multiple sequence aligner] Done")
        
    except Exception as e:
        print(f" [multiple sequence aligner] Error {e}")

        # remove the temporary files
        directory = os.listdir()
        if 'temp.fasta' in directory:
            os.remove('temp.fasta')
        if 'tempout.fasta' in directory:
            os.remove('tempout.fasta')
        if 'tempout.png' in directory:
            os.remove('tempout.png')
        if 'tempout.newick' in directory:
            os.remove('tempout.newick')

        # update pending tasks and completed tasks
        print(f" [multiple sequence aligner] Updating pending and completed tasks...")
        task_num = args['task_number']
        with common_variables.multiple_sequence_align_pending_tasks_lock:
            with open('msa_pending_tasks.json', 'r') as f:
                tasks = json.load(f)
            print(f" [multiple sequence aligner] Pending tasks: {tasks}")
            print(type(tasks))
            if type(tasks) != list:
                with open('msa_pending_tasks.json', 'w') as f:
                    pass
            else:
                print(f" [multiple sequence aligner] Pending tasks: {tasks}")
                tasks = [task for task in tasks if task['task_number'] != task_num]
                with open('msa_pending_tasks.json', 'w') as f:
                    json.dump(tasks, f)

        with common_variables.multiple_sequence_align_completed_tasks_lock:
            with open('msa_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': task_num,
                    'task_name': f'{args["email"]} - {task_num}',
                    'task_type': 'Multiple Sequence Alignment',
                    'task_result': 'Failed',
                    'mail': args['email'],
                    'status': 'Failed',
                }, f)
                f.write('\n')
        
        raise e
    finally:
        msa_channel.basic_ack(delivery_tag=method.delivery_tag)

def start_multiple_seq_align_worker():
    '''
    start the multiple sequence aligner worker

    args:
    
            None
    '''
    global msa_channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_CONFIG['host']))
    msa_channel = connection.channel()
    if msa_channel.queue_declare(queue='multiple_seq_align_queue', durable=True).method.message_count > 0:
        msa_channel.queue_purge(queue='multiple_seq_align_queue')
    msa_channel.queue_declare(queue='multiple_seq_align_queue', durable=True)
    msa_channel.basic_qos(prefetch_count=1)
    msa_channel.basic_consume(queue='multiple_seq_align_queue', on_message_callback=process_multiple_seq_align_task)
    print(' [multiple sequence aligner] Waiting for messages. To exit press CTRL+C')
    msa_channel.start_consuming()


class TestMultipleSeqAlignWithQueue(unittest.TestCase):
    def test_multiple_seq_align_with_queue(self):
        print(os.getcwd())
        fname = "multiple_sequence_align/q1seqs_new.FASTA"
        with open(fname, 'r') as f:
            align_data = f.read()
        args = {
            'align_data': align_data,
            'generate_tree': True,
            'to': ['kkrk90792@gmail.com'],
            'email': 'kkrk90792@gmail.com',
        }
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_CONFIG['host']))
        msa_channel = connection.channel()
        msa_channel.queue_declare(queue='multiple_seq_align_queue', durable=True)
        msa_channel.basic_qos(prefetch_count=1)
        msa_channel.basic_publish(exchange='', routing_key='multiple_seq_align_queue', body=json.dumps(args))

if __name__ == '__main__':
    unittest.main()
