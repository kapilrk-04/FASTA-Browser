import mysql.connector
import subprocess
import asyncio

async def get_valid_parts_fromdb():
    # connect to database
    db_config = {
        'host': '172.18.0.1',    # Docker container is running on localhost
        'user': 'root',
        'password': 'root',
        'database': 'database',
        'port': 8080     # Exposed port from the Docker container
    }

    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(**db_config)
    print("Connected to MySQL database")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    valid_body_query = "SELECT bodyPart FROM fidBodyPartMap GROUP BY bodyPart HAVING COUNT(bodyPart) > 1"
    cursor.execute(valid_body_query)
    valid_body = cursor.fetchall()
    print(valid_body)

    valid_parts_files = {}

    # for each body part, get all the fids
    for body_part in valid_body:
        tmp_str = ""
        body_part = list(body_part)
        body_part = body_part[0]
        print(body_part)
        fid_query = f"SELECT fid FROM fidBodyPartMap WHERE bodyPart = '{body_part}'"
        cursor.execute(fid_query)
        fids = cursor.fetchall()
        print(fids)

        # for each fid, get the sequence
        for fid in fids:
            fid = fid[0]
            print(fid)
            file_query = f"SELECT fastaFile FROM FastaFileDb WHERE fid = '{fid}'"
            cursor.execute(file_query)
            file = cursor.fetchall()
            file[0] = list(file[0])
            with open(f'variation_analyzer/StoredFiles/{file[0][0]}.fasta', 'r') as f:
                tmp_str += f.read()
            tmp_str += '\n'
        valid_parts_files[body_part] = tmp_str

    #print(valid_parts_files)
    valid_parts = list(valid_parts_files.keys())
    #print(valid_parts)

    # close the connection
    connection.close()

    # print(type(valid_parts))
    # print(type(valid_parts_files))

    return valid_parts, valid_parts_files
        
if __name__ == '__main__':
    asyncio.run(get_valid_parts_fromdb())