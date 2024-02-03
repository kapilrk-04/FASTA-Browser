import * as React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './BlastSearch.css';


function BlastSearch() {
    const [file1, setFile1] = useState(null);
    const [data1, setData1] = useState("");
    const [mail, setMail] = useState("");
    const [inMode, setInMode] = useState("");
    const [blastProg, setBlastProg] = useState("");
    const [dB, setDB] = useState("");
    const [numAlign, setNumAlign] = useState(1);

    const handleSingleFile = async (e) => {
        console.log("Single file upload");
        setFile1(e.target.files[0]);
        const reader = new FileReader();
        reader.onload = async (e) => {
            const text = (e.target.result);
            console.log("Reading file 1:")
            setData1(text);
            console.log("File 1 read")
        };

        if (e.target.files[0]) {
            reader.readAsText(e.target.files[0]);
        }
    }

    const handleReset = () => {
        setFile1(null);
        setData1("");
        setMail("");
        setInMode("protein");
        setBlastProg("blastp");
        setDB("swissprot");
        setNumAlign(10);
    }

    const handleUpload = async () => {
        console.log("Upload button clicked");
        console.log("data1:", data1);
        console.log("mail:", mail);
        console.log("inMode:", inMode);
        console.log("blastProg:", blastProg);
        console.log("dB:", dB);
        console.log("numAlign:", numAlign);
        if(data1) {
            let data = {
                fasta_file: data1,
                blast_program : blastProg,
                database : dB,
                num_alignments : numAlign,
                mail : mail
            }
            console.log("Data:", data1);
            try {
                const res = await axios.post("http://127.0.0.1:8000/blast_search", data);
                // console.log(res);
                // setRes(res);

                // const fileContents = `${res.data.per_line_out}`
                // const blob = new Blob([fileContents], {type: 'text/plain'});

                // const url = window.URL.createObjectURL(blob);
                // setDownload(url);
                if (res.status === 200) {
                    window.alert("BLAST search request successfully sent! Check your email for the result.");
                    window.location.href = '/home';
                } else {
                    window.alert("Something went wrong. Please try again.");
                    window.location.href = '/home';
                }

            } catch (err) {
                console.log(err.response);
                window.alert("Something went wrong. Please try again.");
                window.location.href = '/home';

            }
        }
    }
        
    return (
        <div>
            <div className="title-bar">
                <h1>PERFORM BLAST SEARCH</h1>
                <button onClick={() => window.location.href = '/home'}>Home</button>
            </div>

            <div className="form-container">
                <div>
                    <div>
                        <input type="file" accept=".fna, .fasta, .FASTA" onChange={handleSingleFile} />
                        <input type="text" placeholder="Enter email" onChange={(e) => setMail(e.target.value)} />
                        <select onChange={(e) => setInMode(e.target.value)}>
                            <option value="protein">Protein</option>
                            <option value="nucleotide">Nucleotide</option>
                        </select>

                        <select onChange={(e) => setBlastProg(e.target.value)}>
                            <option value="">Select blast program</option>
                            {inMode === "protein" && <option value="blastp">blastp</option>}
                            {inMode === "nucleotide" && <option value="blastn">blastn</option>}
                        </select>

                        <select onChange={(e) => setDB(e.target.value)}>
                            <option value="">Select database</option>
                            {inMode === "protein" && <option value="swissprot">SwissProt</option>}
                            {inMode === "protein" && <option value="nr">NR</option>}
                            {inMode === "protein" && <option value="refseq_protein">RefSeq Protein</option>}
                            {inMode === "nucleotide" && <option value="nt">NT</option>}
                            {inMode === "nucleotide" && <option value="refseq_genomic">RefSeq Genomic</option>}
                        </select>

                        <select onChange={(e) => setNumAlign(e.target.value)}>
                            <option value="">Number of alignments</option>
                            <option value="10">10</option>
                            <option value="20">20</option>
                            <option value="50">50</option>
                        </select>

                        <h6>File</h6>
                        {file1 && <p>{file1.name}</p>}
                        <h6>Data</h6>
                        {data1 && <p>{data1.split('\n').slice(0, 90).join('\n')}</p>}

                        <button onClick={handleUpload}>Upload</button>
                        <button onClick={handleReset}>Reset</button>
                    </div>
                </div>

                
            </div>

        </div>
    );
}

export default BlastSearch;

