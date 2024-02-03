import * as React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './VariationAnalyzer.css';


function VariationAnalyzer() {
    const [file1, setFile1] = useState(null);
    const [data1, setData1] = useState("");
    const [mail, setMail] = useState("");

    const [validParts, setValidParts] = useState([]);
    const [validPartsData, setValidPartsData] = useState({});
    const [selectedPart, setSelectedPart] = useState("");
    const [genTree, setGenTree] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await axios.get("http://127.0.0.1:8000/get_valid_parts");
                console.log(res);
                setValidParts(res.data.valid_parts);
                setValidPartsData(res.data.valid_parts_files);
            } catch (err) {
                console.error("Error in fetching valid parts", err);
                console.log(err.response);
                console.log("eroor in fetching valid parts");
            } finally {

                console.log("Valid parts:", validParts);
                console.log("Valid parts data:", validPartsData);
            }
        }
        fetchData();
        console.log("Valid parts:", validParts);
        console.log("Valid parts data:", validPartsData);
    }, [validParts, validPartsData]);

    const handleReset = () => {
        setFile1(null);
        setData1("");
        setMail("");
        setSelectedPart("");
    }

    const handleUpload = async () => {
        console.log(validPartsData);
        console.log(validParts);
        console.log("Upload button clicked");
        console.log("part:", selectedPart);
        setData1(validPartsData[selectedPart]);
        console.log("data1:", data1);

        if(data1) {
            let data = {
                seqs: data1,
                genTree: genTree,
                mail: mail
            }
            console.log("Data:", data1);
            try {
                const res = await axios.post("http://127.0.0.1:8000/multi_seq_align", data);
                // console.log(res);
                // setRes(res);

                // const fileContents = `${res.data.per_line_out}`
                // const blob = new Blob([fileContents], {type: 'text/plain'});

                // const url = window.URL.createObjectURL(blob);
                // setDownload(url);
                if (res.status === 200) {
                    window.alert("Variation analysis (MSA) request successfully sent! Check your email for the result.");
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
                <h1>VARIATION ANALYZER - SPECIES/REGION WISE</h1>
                <button onClick={() => window.location.href = '/home'}>Home</button>
            </div>

            <div className="form-container">
                <div>
                    <div>
                        <select onChange={(e) => setSelectedPart(e.target.value)}>
                            <option value="">Select a part</option>
                            {validParts.map((part) => {
                                return <option value={part}>{part}</option>
                            })}
                        </select>
                        <input type="text" placeholder="Enter email" onChange={(e) => setMail(e.target.value)} />
                        <input type="checkbox" id="genTree" name="genTree" value="genTree" onChange={(e) => setGenTree(e.target.checked)} />
                        <button onClick={handleUpload}>Upload</button>
                        <button onClick={handleReset}>Reset</button>
                    </div>
                </div>

                
            </div>

        </div>
    );
}

export default VariationAnalyzer;

