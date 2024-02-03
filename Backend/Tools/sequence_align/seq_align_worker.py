import json
import pika
import sys
sys.path.append('../')
sys.path.append('./sequence_align')
from seq_align_module import seq_alignment, blosum62, DNAfull
from send_email_module import send_mail_with_attachment
from rabbitmq_config import RABBITMQ_CONFIG
import matplotlib.pyplot as plt
import os
import unittest

import common_variables

channel = None

def process_seq_align_task(ch, method, properties, body):
    try:
        args = json.loads(body.decode('utf-8'))
        cur_task_number = args['task_number']

        print(" [sequence aligner] Received %r" % args)
        algo, seq1, seq2 = args['algo'], args['seq1'], args['seq2']
        matrix = blosum62 if args['matrix'] == 'blosum62' else DNAfull
        #print(" [x] ARGS: ", algo, seq1, seq2, matrix)
        (sq1, sq2) = seq_alignment(algo, seq1, seq2, matrix)
        print(sq1, sq2)
        print(" [sequence aligner] Alignment done")

        matches = ["|" if sq1[i] == sq2[i] else " " if sq1[i] == '-' or sq2[i] == '-' else "*" for i in range(len(sq1))]
        matches = ''.join(matches)
        lens = len(sq1)

        seq1s = []
        seq2s = []
        matchs = []

        i = 0
        while i < lens:
            seq1s.append(sq1[i:i+50])
            seq2s.append(sq2[i:i+50])
            matchs.append(matches[i:i+50])
            i += 50

        per_line_out = [seq1s[i] + "\n" + matchs[i] + "\n" + seq2s[i] + "\n\n" for i in range(len(seq1s))]
        per_line_out = "".join(per_line_out)

        print(" [sequence aligner] Done")
        
        email_result = {
            'seq1': seq1,
            'seq2': seq2,
            'per_line_out': per_line_out
        }

        formatted_str = f"Seq1: {email_result['seq1']}\n" \
            f"Seq2: {email_result['seq2']}\n" \
            f"Alignment:\n{email_result['per_line_out']}"
        
        print(" [sequence aligner] Generating color coded alignment...")

        color_coded_seq_align(sq1, sq2, 'tempout.png')

        print(" [sequence aligner] Sending email...")

        cur_task_number = args['task_number']
        print(f" [sequence aligner] Task number: {cur_task_number}")

        send_mail_with_attachment(
            to=args['to'], 
            subject=f"Sequence Alignment Result for Task {cur_task_number}", 
            body=f"<p>Sequence Alignment Result for Task {cur_task_number}</p>",
            attachment_data=formatted_str.encode('utf-8'),
            attachment_name='seq_align_result.txt', 
            to_mail=args['to_mail'],
            imgpath='tempout.png'
        )

        print(" [sequence aligner] Done")

        # update pending tasks and completed tasks

        print(f" [sequence aligner] Updating pending and completed tasks...")

        with common_variables.sequence_align_pending_tasks_lock:
            with open('sequence_align_pending_tasks.json', 'r') as f:
                tasks = json.load(f)
            print(f" [sequence aligner] Pending tasks: {tasks}")
            print(type(tasks))
            if type(tasks) != list:
                with open('sequence_align_pending_tasks.json', 'w') as f:
                    pass
            else:
                print(f" [sequence aligner] Pending tasks: {tasks}")
                tasks = [task for task in tasks if task['task_number'] != cur_task_number]
                with open('sequence_align_pending_tasks.json', 'w') as f:
                    json.dump(tasks, f)

        with common_variables.sequence_align_completed_tasks_lock:
            with open('sequence_align_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': cur_task_number,
                    'task_name': f'{args["to_mail"]} - {cur_task_number}',
                    'task_type': 'Sequence Alignment',
                    'task_result': 'Success',
                    'mail': args['to_mail'],
                    'status': 'Success',
                }, f)
                f.write('\n')



        print(f" [sequence aligner] Done")
        print(f" [sequence aligner] Task {cur_task_number} completed")

    except Exception as e:
        print(f" [sequence aligner] Error {e}")

        # update pending tasks and completed tasks
        print(f" [sequence aligner] Updating pending and completed tasks...")
        with common_variables.sequence_align_pending_tasks_lock:
            with open('sequence_align_pending_tasks.json', 'r') as f:
                tasks = json.load(f)
            print(f" [sequence aligner] Pending tasks: {tasks}")
            print(type(tasks))
            if type(tasks) != list:
                with open('sequence_align_pending_tasks.json', 'w') as f:
                    pass
            else:
                print(f" [sequence aligner] Pending tasks: {tasks}")
                tasks = [task for task in tasks if task['task_number'] != cur_task_number]
                with open('sequence_align_pending_tasks.json', 'w') as f:
                    json.dump(tasks, f)

        with common_variables.sequence_align_completed_tasks_lock:
            with open('sequence_align_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': cur_task_number,
                    'task_name': f'{args["to_mail"]} - {cur_task_number}',
                    'task_type': 'Sequence Alignment',
                    'task_result': 'Failure',
                    'mail': args['to_mail'],
                    'status': 'Failure',
                }, f)
                f.write('\n')

        raise e
    finally:
        channel.basic_ack(delivery_tag=method.delivery_tag)
        



def color_coded_seq_align(seq1, seq2, outfile):
    fig, ax = plt.subplots(figsize=(15, 6))  # Adjust figure size as needed
    chunk_size = 50
    y_offset = 0.05  # Adjust the y_offset for line spacing
    font_size = 10  # Adjust the font size

    for i in range(0, len(seq1), chunk_size):
        chunk_end = min(i + chunk_size, len(seq1))
        s1 = seq1[i:chunk_end]
        s2 = seq2[i:chunk_end]

        for j, (c1, c2) in enumerate(zip(s1, s2)):
            if c1 == c2:
                color = 'green'
            elif c1 == '-' or c2 == '-':
                color = 'orange'
            else:
                color = 'magenta'

            ax.text(j + 0.05, -0.05 - y_offset, c1, color=color, ha='center', va='center', fontsize=font_size, bbox=dict(facecolor='none', edgecolor='none'))
            ax.text(j + 0.05, -0.15 - y_offset, c2, color=color, ha='center', va='center', fontsize=font_size, bbox=dict(facecolor='none', edgecolor='none'))

        y_offset += 0.3

    ax.set_yticks([])
    ax.set_xlim([-1, chunk_size * 2])

    ax.axis('off')

    plt.savefig(outfile, format='png')  



def start_seq_align_worker():
    configs = RABBITMQ_CONFIG
    global channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=configs['host'], 
        port=configs['port'],
        credentials=pika.PlainCredentials(configs['username'], configs['password'])))
    
    channel = connection.channel()
    channel.queue_delete(queue=configs['seq_align_queue'])
    channel.queue_declare(queue=configs['seq_align_queue'], durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=configs['seq_align_queue'], on_message_callback=process_seq_align_task)

    print(' [sequence aligner] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

class TestSequenceAlignWithQueue(unittest.TestCase):
    def test_sequence_align_with_queue(self):
        try:
            msg = {
                'algo': 'needleman_wunsch',
                'seq1': '>s1\nACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGACACCGGTGAC',
                'seq2': '>s2\nACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGACACGTGAC',
                'matrix': 'blosum62',
                'to': ['kkrk90792@gmail.com'],
                'to_mail': 'kkrk90792@gmail.com'
            }
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=RABBITMQ_CONFIG['host'], 
                port=RABBITMQ_CONFIG['port'],
                credentials=pika.PlainCredentials(RABBITMQ_CONFIG['username'], RABBITMQ_CONFIG['password'])))
            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_CONFIG['seq_align_queue'], durable=True)
            channel.basic_publish(exchange='', routing_key=RABBITMQ_CONFIG['seq_align_queue'], body=json.dumps(msg))
            print(" [x] Sent 'Hello World!'")
            connection.close()
        except Exception as e:
            print(e)
            self.fail()
        finally:
            pass

if __name__ == '__main__':
    unittest.main()
    
