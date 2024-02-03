# Software Requirements Specification (SRS) Document 

### Team NaClStack   
### Shreyas Badami, Kapil Rajesh Kavitha

## Running the project
1. Clone the repository
2. Run `docker-compose up --build` in the root directory
3. Open `localhost:3000` in your browser
4. To stop the project, run `docker-compose down` in the root directory
5. If you run into issues with database content, open MySQL server on your machine and import the contents of `database.sql` in the `database` database

### to run the project without docker
1. Clone the repository

#### Webserver
2. Go to the `Website` directory and run `npm install`
3. Run `npm start` to start the frontend
4. Open `localhost:3000` in your browser

#### Backend (Python)
5. Go to the `Backend/Tools` directory and run `pip install -r requirements.txt`
6. Run `uvicorn main:app --reload --host 0.0.0.0 --port 8000` to start the backend FastAPI server
7. Open another terminal and go to the `Backend/Tools` directory and run `python3 starter.py` to start the RabbitMQ services and initialize all the log files

#### Backend (SQL)
8. Go to the `Backend/Database' directory
9. Run MySQL server on your machine and import the `database.sql` file in the 'database' database


### Project Structure

#### Website
1. `Website` directory contains the frontend code
2. `Website/src` contains the React code 
3. The components are as follows: 
    - `blastsearch` - contains the code for the blast search page
    - `compare` - contains the code for the pairwise alignment page
    - `generate_tree` - contains the code for the phylogenetic tree generation page
    - `homepage` - contains the code for the homepage
    - `login` - contains the code for the login page (authentication doesn't work but can be integrated with the API)
    - `multiple_align` - contains the code for the multiple sequence alignment page
    - `variationanalysis` - contains the code for the variation analysis page
    - `viewqueues` - contains the code for the page to view queue logs
4. `App.js` contains the code for the navigation bar and routing
5. `index.js` contains the code for the root component

#### Backend
1. `Backend` directory contains the backend code
2. `Backend/Tools` contains the code for the FastAPI server and RabbitMQ services
3. `Backend/Database` contains the code for the MySQL database

#### FastAPI server and RabbitMQ services
1. `Backend/Tools/main.py` contains the code for the FastAPI server. The following API calls are implemented:
    - `/seq_align` - API call to perform pairwise alignment
    - `/multi_seq_align` - API call to perform multiple sequence alignment
    - `/phylo_tree` - API call to generate phylogenetic tree
    - `/blast_search` - API call to perform BLAST search
    - `/get_valid_parts` - API call used to get the valid body parts from created database: used for variation analysis
    - `/get_queue_info` - API call used to get the queue information from the database
2. `Backend/Tools/starter.py` contains the code to start the RabbitMQ services and initialize all the log files
    - For logging purposes, we have used a separate log file for each API call. These are currently stored in the same directory but can be moved to a logs directory in the future. The logs are separate for pending tasks and completed tasks.
    - The log files are named as follows:
        - `blast_pending_tasks.json`
        - `blast_completed_tasks.json`
        - `msa_pending_tasks.json`
        - `msa_completed_tasks.json`
        - `sequence_align_pending_tasks.json`
        - `sequence_align_completed_tasks.json`
        - `phylo_tree_pending_tasks.json`
        - `phylo_tree_completed_tasks.json`
    - The log files are in JSON format and contain the following information:
        - `task_number` - unique id for each task
        - `task_name` - name of the task
        - `task_status` - status of the task (pending/completed)
        - `task_description` - description of the task
        -`task_result` - result of the task (can be used to store link to the result file later)
3. Separate directories are created for each function in the `Backend/Tools` directory. These directories contain the code for the methods and for the RabbitMQ services for each function. The following directories are present:
    - `blast_search` - contains the code for the BLAST search 
        - `blast_search_module` - contains the code for the BLAST search implementation, uses the NCBI server
        - `blast_search_worker` - contains the code for the RabbitMQ service for the BLAST search

    - `multiple_sequence_align` - contains the code for the multiple sequence alignment RabbitMQ service
        - `multiple_seq_align_module` - contains the code for the multiple sequence alignment implementation, uses the Clustal Omega which is installed along with the docker image
        - `multiple_seq_align_worker` - contains the code for the RabbitMQ service for the multiple sequence alignment

    - `phylo_tree` - contains the code for the phylogenetic tree generation
        - `phylotree` - contains the code for the phylogenetic tree generation implementation, uses the Clustal Omega which is installed along with the docker image
        - `phylotree_worker` - contains the code for the RabbitMQ service for the phylogenetic tree generation

    - `sequence_align` - contains the code for the pairwise alignment RabbitMQ service
        - `seq_align_module` - contains the code for the pairwise alignment implementation, uses the Clustal Omega which is installed along with the docker image
        - `seq_align_worker` - contains the code for the RabbitMQ service for the pairwise alignment

    - `variation_analysis` - contains the code for the variation analysis
        - `StoredFiles` directory - contains the FASTA files whose names are present in the database
        - `va_module` - contains the code for the variation analysis implementation: gets the valid body parts from the database and performs MSA on the FASTA files present in the `StoredFiles` directory (pairwise alignment can also be possibly implemented here)

#### MySQL database
1. `Backend/Database/database.sql` contains the code to create the database and the tables
2. The tables present:
    - `FastaFileDb` - contains the names of the FASTA files present in the `StoredFiles` directory, along with details such as the body part, species, etc.
    - `fidBodyPartMap` - contains the mapping between the FASTA file names and the body parts. Used for variation analysis search purposes.
    - `fidKeywordMap` - contains the mapping between the FASTA file names and the keywords. Used for variation analysis search purposes.
    - `humanReferenceGenome` - contains the human reference genome in chromosome-wise FASTA files. Currently not present due to large size of the files, but can be added with addition of cloud storage resources.
3. Currently only MSA on all FASTA files for a given body part is implemented. Pairwise alignment can be implemented by using the `fidBodyPartMap` table to get 2 FASTA files for a given body part and performing pairwise alignment on them.

#### General implementation details

1. This project aims to implement a request-based interface: the user can submit a request for a task to be performed, and the result is generated and sent to the user by mail. The user can also view the status of the task in the queue logs.
2. The user can also view the queue logs to see the status of the tasks in the queue. The queue logs are updated on refreshing, and they are maintained using the provided JSON files (a database implementation can be added later)
3. The request-based interface is implemented using RabbitMQ. The RabbitMQ services are implemented using the `pika` library.
4. The RabbitMQ services are implemented as follows:
    - The user submits a request for a task to be performed
    - The request is sent to the RabbitMQ service
    - The RabbitMQ service adds the task to the queue and returns a task number to the user
    - The user can use the task number to view the status of the task in the queue logs
    - The RabbitMQ service performs the task and updates the queue logs
    - SMTPLib is used to send the result to the user by mail

#### Feature implementations:
1. Pairwise alignment
    - Take 1 or 2 FASTA files as input. If 1 file is given, the file must contain 2 sequences. If 2 files are given, each file must contain 1 sequence.
    - 2 output files are generated: 1) A text file containing the aligned sequences, 2) an image file containing the alignment visualization with color coding
    - Two alignment methods are implemented: 1) Global alignment (needleman-wunsch algorithm), 2) Local alignment (smith-waterman algorithm)
    - The alignment method can be selected by the user
    - The matrix used for alignment can be selected by the user

2. Multiple sequence alignment
    - Take a single FASTA file as input. The file must contain `n` sequences.
    - Clustal Omega is used for multiple sequence alignment, this is installed along with the docker image. The BioPython library is used to access Clustal Omega command line given that Clustal Omega is installed.
    - An option to generate a phylogenetic tree is also provided. If the user selects this option, the phylogenetic tree is generated in addition to the multiple sequence alignment.
    - 2/3 output files are generated: 1) A text file containing the aligned sequences, 2) an image file containing the alignment visualization with color coding, 3) a text file containing the phylogenetic tree in ASCII (if selected)

3. Phylogenetic tree generation
    - Take a single FASTA file as input. The file must contain `n` sequences which have been aligned.
    - Generated using BioPython library
    - 1 file is generated: an text file containing the phylogenetic tree in ASCII

4. BLAST search
    - Take a single FASTA file as input. The file must contain 1 sequence.
    - NCBI server is used for BLAST search, this is accessed using the Biopython library.
    - The user can select multiple argumenta:
        - Protein/nucleotide sequence input
        - Database to search in (nt, nr, etc.)
        - Algorithm to use (blastn, blastp)
        - Number of results to return (10, 20, 50, etc.)
    - 1 file is generated: a text file containing the BLAST search results.
    - This typically takes a long time to run, so the user is redirected to the home page.

5. Variation analysis
    - Here, `get_valid_parts` API call is used to get the valid body parts from the database. These body parts are those that have 2 or more entries in the `FastaFileDb` table. 
    - The user can select a body part from the dropdown menu. The FASTA files corresponding to the selected body part are then used for multiple sequence alignment.
    - Similar to multiple sequence alignment, the user can select an option to generate a phylogenetic tree.
    - 2/3 output files are generated: 1) A text file containing the aligned sequences, 2) an image file containing the alignment visualization with color coding, 3) a text file containing the phylogenetic tree in ASCII (if selected)


#### Improvements to be made
1. The database can be implemented using cloud storage resources such as AWS S3. This will allow us to store the human reference genome and the FASTA files in the database.
2. The implementation for avoiding too many requests to the server is currently buggy, due to improper reading of the queue logs. This can be fixed by using a database implementation for the queue logs. (current implementation can also be fixed)
3. The queue logs can be implemented using a database instead of JSON files. This will allow us to store more information about the tasks, and will be safer
4. Instead of sending results by mail, the results can be stored in the database and the user can be redirected to a page where they can view the results.
5. The user authentication can be implemented using the API provided by DataFoundationSystem.
6. For variation analysis, the user can be allowed to select 2 body parts and the FASTA files corresponding to the selected body parts can be used for pairwise alignment.


