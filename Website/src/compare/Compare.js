import * as React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Compare.css';


function Compare() {
    const [one, setOne] = useState(false);
    const [two, setTwo] = useState(false);

    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);

    const [data1, setData1] = useState("");
    const [data2, setData2] = useState("");
    const [algo, setAlgo] = useState("");
    const [matrix, setMatrix] = useState("");

    const [res, setRes] = useState(null);
    const [download, setDownload] = useState(null);

    const [mail, setMail] = useState("");
    const [sendMail, setSendMail] = useState(false);

    const handleClickOne = () => {
        if(!one) {
            setOne(true);
            setTwo(false);
        } else {
            setOne(false);
            setTwo(false);
        }
        handleReset();
        console.log("one:", one);
        console.log("two:", two);
    }

    const handleClickTwo = () => {
        if(!two) {
            setTwo(true);
            setOne(false);
        } else {
            setTwo(false);
            setOne(false);
        }
        handleReset();
        console.log("one:", one);
        console.log("two:", two);
    }

    const handleSingleFile = async (e) => {
        console.log("Single file upload");
        setFile1(e.target.files[0]);
        const reader = new FileReader();
        reader.onload = async (e) => {
            const text = (e.target.result);
            console.log("Reading file 1:")
            let texts = text.split(">");
            console.log("texts:", texts);
            setData1(texts[1]);
            console.log("File 1 read")
            console.log("data1:", data1);
            setData2(texts[2]);
            console.log("data2:", data2);
        };

        if (e.target.files[0]) {
            reader.readAsText(e.target.files[0]);
        }
    }
    const handleFile1 = async (e) => {
        setFile1(e.target.files[0]);
        const reader = new FileReader();
        reader.onload = async (e) => {
            const text = (e.target.result);
            console.log("Reading file 1:")
            setData1(text);
            console.log("File 1 read")
            console.log("data1:", data1);
        };
        if (e.target.files[0]) {
            reader.readAsText(e.target.files[0]);
        }
    };

    const handleFile2 = async (e) => {
        setFile2(e.target.files[0]);
        console.log(file2)
        const reader = new FileReader();
        reader.onload = async (e) => {
            const text = (e.target.result);
            setData2(text);
            console.log("File 2 read")
            console.log("data2:", data2);
        };
        if (e.target.files[0]) {
            reader.readAsText(e.target.files[0]);
        }
    };

    const handleReset = () => {
        setFile1(null);
        setFile2(null);
        setData1("");
        setData2("");
        setAlgo("");
        setMatrix("");
        setRes(null);
        setDownload(null);
        setMail("");
        setSendMail(false);
    }

    const handleUpload = async () => {
        console.log("Upload button clicked");
        console.log("data1:", data1);
        console.log("data2:", data2);
        console.log("algo:", algo);
        console.log("matrix:", matrix);
        if(data1 && data2 && algo && matrix) {
            let data = {
                seq1: data1,
                seq2: data2,
                matrix: matrix,
                algo: algo,
                mail: mail
            }
            console.log("Data:", data);
            try {
                const res = await axios.post("http://127.0.0.1:8000/seq_align", data);
                // console.log(res);
                // setRes(res);

                // const fileContents = `${res.data.per_line_out}`
                // const blob = new Blob([fileContents], {type: 'text/plain'});

                // const url = window.URL.createObjectURL(blob);
                // setDownload(url);
                if (res.status == 200){
                    window.alert("Alignment request successfully sent! Check your email for the result.");
                    window.location.href = '/home';
                } else {
                    window.alert("Alignment request failed. Please try again.");
                    window.location.href = '/home';
                }

            } catch (err) {
                console.log(err.response);
                window.alert("Alignment request failed. Please try again.");
                window.location.href = '/home';
            }
        }
    }
        
    return (
        <div>
            <div className="title-bar">
                <h1>Compare 2 sequences (ALIGNMENT)</h1>
                <button onClick={() => window.location.href = '/home'}>Home</button>
            </div>

            <div className="form-container">
                <div class="num-files">
                    <label htmlFor="num-files">Number of files:</label>
                    <button onClick={handleClickOne}>1</button>
                    <button onClick={handleClickTwo}>2</button>
                </div>

                {two && <div>
                    <div>
                        <input type="file" accept=".fna, .fasta, .FASTA" onChange={handleFile1} />
                        <h6>File 1</h6>
                        {file1 && <p>{file1.name}</p>}
                        <h6>Data 1</h6>
                        {data1 && <p>{data1.split('\n').slice(0, 20).join('\n')}</p>}
                        <input type="file" accept=".fna, .fasta, .FASTA" onChange={handleFile2} />
                        <h6>File 2</h6>
                        {file2 && <p>{file2.name}</p>}
                        <h6>Data 2</h6>
                        {data2 && <p>{data2.split('\n').slice(0, 20).join('\n')}</p>}

                        <div class="dropdown">
                            <label htmlFor="algo">Choose an algorithm:</label>
                            <select name="algo" id="algo" value={algo} onChange={(e) => setAlgo(e.target.value)}>
                                <option value="">Select an algorithm</option>
                                <option value="needleman_wunsch">Needleman-Wunsch</option>
                                <option value="smith_waterman">Smith-Waterman</option>
                            </select>
                        </div>

                        <div class="dropdown">
                            <label htmlFor="matrix">Choose a matrix:</label>
                            <select name="matrix" id="matrix" value={matrix} onChange={(e) => setMatrix(e.target.value)}>
                                <option value="">Select a matrix</option>
                                <option value="blosum62">BLOSUM62</option>
                                <option value="DNAfull">DNAfull</option>
                            </select>
                        </div>

                        <div>
                            <input type="email" placeholder="Enter your email" onChange={(e) => setMail(e.target.value)} />
                        </div>

                        <button onClick={handleUpload}>Upload</button>
                        <button onClick={handleReset}>Reset</button>
                    </div>
                </div>}

                {one && <div>
                    <div>
                        <input type="file" accept=".fna, .fasta, .FASTA" onChange={handleSingleFile} />
                        <h6>File</h6>
                        {file1 && <p>{file1.name}</p>}
                        <h6>Data</h6>
                        {data1 && <p>{data1.split('\n').slice(0, 90).join('\n')}</p>}
                        <div class="dropdown">
                            <label htmlFor="algo">Choose an algorithm:</label>
                            <select name="algo" id="algo" value={algo} onChange={(e) => setAlgo(e.target.value)}>
                                <option value="">Select an algorithm</option>
                                <option value="needleman_wunsch">Needleman-Wunsch</option>
                                <option value="smith_waterman">Smith-Waterman</option>
                            </select>
                        </div>

                        <div class="dropdown">
                            <label htmlFor="matrix">Choose a matrix:</label>
                            <select name="matrix" id="matrix" value={matrix} onChange={(e) => setMatrix(e.target.value)}>
                                <option value="">Select a matrix</option>
                                <option value="blosum62">BLOSUM62</option>
                                <option value="DNAfull">DNAfull</option>
                            </select>
                        </div>

                        <div>
                            <input type="email" placeholder="Enter your email" onChange={(e) => setMail(e.target.value)} />
                        </div>

                        <button onClick={handleUpload}>Upload</button>
                        <button onClick={handleReset}>Reset</button>
                    </div>
                </div>}

                
            </div>

            {res && <div className='result-container'>
                <h3>ALIGNMENT result</h3>
                <p class="aligned-text">{res.data.per_line_out}</p>
            </div>}

            {download && <div className='download-container'>
                <a href={download} download="alignment_result.txt">Download result</a>
            </div>}

        </div>
    );
}

export default Compare;

