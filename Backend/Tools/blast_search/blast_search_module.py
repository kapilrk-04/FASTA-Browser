from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML
import io
import os
import threading

blast_lock = threading.Lock()

def perform_blast_search(fasta_file, output_file, blast_program='blastn', database='nr', num_alignments=10):

    '''
    Perform BLAST search and write the result to a file

    args:

    fasta_file: .FASTA file with input sequence
    output_file: .txt file to write the BLAST result to
    blast_program: BLAST program to use
    database: BLAST database to use
    num_alignments: number of alignments to return

    '''
    # Read the sequence from the FASTA file
    print(f" [blast search] Reading FASTA file...")
    print(os.getcwd())
    record = SeqIO.read(fasta_file, format="fasta")
    sequence = record.seq
    
    print(f" [blast search] Performing BLAST search...")
    print(f" [blast search] blast_program: {blast_program}")
    print(f" [blast search] database: {database}")
    print(f" [blast search] num_alignments: {num_alignments}")
    print(f" [blast search] sequence: {sequence}")
    # Perform BLAST search
    with blast_lock:
        result_handle = NCBIWWW.qblast(blast_program, database, sequence, alignments=num_alignments)

        # Parse and print the BLAST result
        blast_records = NCBIXML.read(result_handle)
        print(f" [blast search] Writing to file...")
        with open(output_file, 'w') as f:
            for alignment in blast_records.alignments:
                for hsp in alignment.hsps:
                    f.write(f"****Alignment****\n")
                    f.write(f"Sequence: {alignment.title}\n")
                    f.write(f"Length: {alignment.length}\n")
                    f.write(f"E-value: {hsp.expect}\n")
                    for i in range(0, len(hsp.query), 50):
                        if i + 50 < len(hsp.query):
                            f.write(f"{hsp.query[i:i+50]}\n")
                            f.write(f"{hsp.match[i:i+50]}\n")
                            f.write(f"{hsp.sbjct[i:i+50]}\n")
                        else:
                            f.write(f"{hsp.query[i:]}\n")
                            f.write(f"{hsp.match[i:]}\n")
                            f.write(f"{hsp.sbjct[i:]}\n")
                        f.write(f"\n")
                    
                    f.write(f"\n")

        # Close the result handle
        result_handle.close()

# Replace 'input_sequence.fasta' with your file path
if __name__ == '__main__':
    input_fasta_file = 'q1seqs.FASTA'

    out_file = "blast_result.txt"
    perform_blast_search(input_fasta_file, out_file)
# # Perform BLAST search and print the results
# perform_blast_search(input_fasta_file)
