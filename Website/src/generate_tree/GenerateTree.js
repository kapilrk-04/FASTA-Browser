import * as React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './GenerateTree.css';


function Generate_Tree() {
    const [file1, setFile1] = useState(null);
    const [data1, setData1] = useState("");
    const [mail, setMail] = useState("");

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
    }

    const handleUpload = async () => {
        console.log("Upload button clicked");
        console.log("data1:", data1);
        if(data1) {
            let data = {
                seqs: data1,
                mail: mail
            }
            console.log("Data:", data1);
            try {
                const res = await axios.post("http://127.0.0.1:8000/phylo_tree", data);
                // console.log(res);
                // setRes(res);

                // const fileContents = `${res.data.per_line_out}`
                // const blob = new Blob([fileContents], {type: 'text/plain'});

                // const url = window.URL.createObjectURL(blob);
                // setDownload(url);
                if (res.status === 200) {
                    window.alert("Phylogenetic tree generation request successfully sent! Check your email for the result.");
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
                <h1>GENERATE PHYLOGENETIC TREE</h1>
                <button onClick={() => window.location.href = '/home'}>Home</button>
            </div>

            <div className="form-container">
                <div>
                    <div>
                        <input type="file" accept=".fna, .fasta, .FASTA" onChange={handleSingleFile} />
                        <input type="text" placeholder="Enter email" onChange={(e) => setMail(e.target.value)} />
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

export default Generate_Tree;

