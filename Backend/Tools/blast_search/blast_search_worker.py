import json
import pika
import sys
sys.path.append('../')
sys.path.append('./blast_search')
from blast_search_module import perform_blast_search
from send_email_module import send_mail_with_attachment
import time
from rabbitmq_config import RABBITMQ_CONFIG
import os

import common_variables

blast_channel = None

def process_blast_search_task(ch, method, properties, body):

    '''
    args:
        body: {
            'fasta_file': fasta_file,
            'blast_program': blast_program,
            'database': database,
            'num_alignments': num_alignments,
            'to': [mail],
            'email': email,
            'task_number': task_number,
        }

    '''
    try:
        # get arguments
        args = json.loads(body.decode('utf-8'))
        print(" [blast search] Received %r" % args)
        inputs, blast_program, database, num_alignments = args['fasta_file'], args['blast_program'], args['database'], args['num_alignments']
        
        # write arguments to a temporary file which will be used for the BLAST search
        fasta_file = 'q1seqs.FASTA'
        with open(fasta_file, 'w') as f:
            f.write(inputs)
        out_file = 'blast_out.txt'
        
        # perform BLAST search
        print(" [blast search] Performing BLAST search...")
        perform_blast_search(fasta_file, out_file, blast_program, database, num_alignments)

        # read the output file and send it as an email attachment
        print(" [blast search] Sending email...")

        blast_out = ''
        with open(out_file, 'r') as f:
            blast_out = f.read()

        formatted_str = f"{blast_out}"

        send_mail_with_attachment(
            to=args['to'],
            subject='BLAST Search Result',
            body='<p>BLAST Search Result</p>',
            attachment_data=bytes(formatted_str, 'utf-8'),
            attachment_name='blast_search_result.txt',
            to_mail=args['email'],
        )

        # update pending and completed tasks
        print(" [blast search] Updating pending and completed tasks...")

        with common_variables.blast_search_pending_tasks_lock:
            with open('blast_pending_tasks.json', 'r') as f:
                pending_tasks = json.loads(f.read())
            if type(pending_tasks) != list:
                with open('blast_pending_tasks.json', 'w') as f:
                    pass
            else:
                pending_tasks = [task for task in pending_tasks if task['task_number'] != args['task_number']]
                with open('blast_pending_tasks.json', 'w') as f:
                    json.dump(pending_tasks, f)

        with common_variables.blast_search_completed_tasks_lock:
            with open('blast_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': args['task_number'],
                    'task_name': f'{args["email"]} - {args["task_number"]}',
                    'task_type': 'BLAST Search',
                    'task_result': 'Success',
                    'mail': args['email'],
                    'status': 'Success',
                }, f)
                f.write('\n')

        print(" [blast search] Done")
    except Exception as e:
        print(" [blast search] Error: %r" % e)

        print(" [blast search] Updating pending and completed tasks...")
        with common_variables.blast_search_pending_tasks_lock:
            with open('blast_pending_tasks.json', 'r') as f:
                pending_tasks = json.loads(f.read())
            if type(pending_tasks) != list:
                with open('blast_pending_tasks.json', 'w') as f:
                    pass
            else:
                pending_tasks = [task for task in pending_tasks if task['task_number'] != args['task_number']]
                with open('blast_pending_tasks.json', 'w') as f:
                    json.dump(pending_tasks, f)

        with common_variables.blast_search_completed_tasks_lock:
            with open('blast_completed_tasks.json', 'a') as f:
                json.dump({
                    'task_number': args['task_number'],
                    'task_name': f'{args["email"]} - {args["task_number"]}',
                    'task_type': 'BLAST Search',
                    'task_result': 'Failed',
                    'mail': args['email'],
                    'status': 'Failed',
                }, f)
                f.write('\n')
    finally:
        blast_channel.basic_ack(delivery_tag=method.delivery_tag)
        if os.path.exists(fasta_file):
            os.remove(fasta_file)
        if os.path.exists(out_file):
            os.remove(out_file)
        

def start_blast_search_worker():
    global blast_channel
    while True:
        try:
            blast_channel = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_CONFIG['host'])).channel()
            blast_channel.queue_declare(queue='blast_search_queue', durable=True)
            blast_channel.basic_qos(prefetch_count=1)
            blast_channel.basic_consume(queue='blast_search_queue', on_message_callback=process_blast_search_task, auto_ack=False)
            print(' [BLAST search] Waiting for messages. To exit press CTRL+C')
            blast_channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(" [BLAST search] Connection error: %r" % e)
            time.sleep(5)
        except pika.exceptions.StreamLostError as e:
            print(" [BLAST search] Stream lost error: %r" % e)
            time.sleep(5)
        except KeyboardInterrupt:
            # Handle user interruption (e.g., CTRL+C) gracefully
            print(" [BLAST search] Worker interrupted. Exiting...")
            break

        except Exception as generic_error:
            # Handle other unexpected errors
            print(f"Unexpected error: {generic_error}")
            break

        finally:
            # Close the channel and connection in case of a clean exit or unexpected error
            if blast_channel.is_open:
                blast_channel.close()

# sample usage
if __name__ == '__main__':
    in_file = 'blast_search/q1seqs.FASTA'
    out_file = 'blast_out.txt'
    blast_program = 'blastn'
    database = 'nt'
    num_alignments = 10
    if os.path.exists(in_file):
        with open(in_file, 'r') as f:
            inputs = f.read()
    args = {
        'fasta_file': inputs,
        'blast_program': blast_program,
        'database': database,
        'num_alignments': num_alignments,
        'to': ['kkrk90792@gmail.com'],
        'email': 'kkrk90792@gmail.com'
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_CONFIG['host'], heartbeat=0, blocked_connection_timeout=0))
    blast_channel = connection.channel()
    blast_channel.queue_declare(queue='blast_search_queue', durable=True)
    blast_channel.basic_qos(prefetch_count=1)
    blast_channel.basic_publish(exchange='', routing_key='blast_search_queue', body=json.dumps(args), properties=pika.BasicProperties(delivery_mode=2))
    print(f" [BLAST search] Sent 'Hello World!' at {time.time()}")
