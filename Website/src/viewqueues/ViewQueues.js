import * as React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './ViewQueues.css';

function ViewQueues() {
    const [seqAlignPendingList, setSeqAlignPendingList] = useState([]);
    const [seqAlignCompletedList, setSeqAlignCompletedList] = useState([]);
    const [MSAPendingList, setMSAPendingList] = useState([]);
    const [MSACompletedList, setMSACompletedList] = useState([]);
    const [blastPendingList, setBlastPendingList] = useState([]);
    const [blastCompletedList, setBlastCompletedList] = useState([]);
    const [phyloPendingList, setPhyloPendingList] = useState([]);
    const [phyloCompletedList, setPhyloCompletedList] = useState([]);
    const [hasFetched, setHasFetched] = useState(false);

    React.useEffect(() => {
        const fetchQueues = async () => {
            try {
                const res = await axios.get("http://127.0.0.1:8000/get_queue_info");
                setSeqAlignPendingList(res.data.seq_align_pending_tasks);
                setSeqAlignCompletedList(res.data.seq_align_completed_tasks);
                setMSAPendingList(res.data.multiple_seq_align_pending_tasks);
                setMSACompletedList(res.data.multiple_seq_align_completed_tasks);
                setBlastPendingList(res.data.blast_search_pending_tasks);
                setBlastCompletedList(res.data.blast_search_completed_tasks);
                setPhyloPendingList(res.data.phylo_tree_pending_tasks);
                setPhyloCompletedList(res.data.phylo_tree_completed_tasks);
                setHasFetched(true);
            } catch (err) {
                console.error("Error in fetching queues", err);
                console.log(err.response);
                console.log("eroor in fetching queues");
            } finally {
                console.log("Seq align pending:", seqAlignPendingList);
                console.log("Seq align completed:", seqAlignCompletedList);
                console.log("MSA pending:", MSAPendingList);
                console.log("MSA completed:", MSACompletedList);
                console.log("Blast pending:", blastPendingList);
                console.log("Blast completed:", blastCompletedList);
                console.log("Phylo pending:", phyloPendingList);
                console.log("Phylo completed:", phyloCompletedList);
            }
        }
        fetchQueues();
    }, [hasFetched]);
        
    return (
        <div>
            <div className="title-bar">
                VIEW QUEUE LOGS
            </div>

            <div className="queue-container">
                <div className="queue-title">
                    Sequence Alignment
                </div>
                {seqAlignPendingList.length > 0 && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Pending
                        </div>
                        <div className="queue-list-items">
                            {seqAlignPendingList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {(seqAlignCompletedList.length > 0) && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Completed
                        </div>
                        <div className="queue-list-items">
                            {seqAlignCompletedList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="queue-title">
                    Multiple Sequence Alignment
                </div>
                {MSAPendingList.length > 0 && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Pending
                        </div>
                        <div className="queue-list-items">
                            {MSAPendingList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {(MSACompletedList.length > 0) && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Completed
                        </div>
                        <div className="queue-list-items">
                            {MSACompletedList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="queue-title">
                    Blast Search
                </div>
                {blastPendingList.length > 0 && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Pending
                        </div>
                        <div className="queue-list-items">
                            {blastPendingList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {(blastCompletedList.length > 0) && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Completed
                        </div>
                        <div className="queue-list-items">
                            {blastCompletedList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="queue-title">
                    Phylogenetic Tree
                </div>
                {phyloPendingList.length > 0 && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Pending
                        </div>
                        <div className="queue-list-items">
                            {phyloPendingList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {(phyloCompletedList.length > 0) && (
                    <div className="queue-list">
                        <div className="queue-list-title">
                            Completed
                        </div>
                        <div className="queue-list-items">
                            {phyloCompletedList.map((item, index) => (
                                <div className="queue-list-item" key={index}>
                                    <p><b>Task ID:</b> {item.task_number}</p>
                                    <p><b>Task Name:</b> {item.task_name}</p>
                                    <p><b>Task Description:</b> {item.task_type}</p>
                                    <p><b>Task Status:</b> {item.task_status}</p>
                                    <p><b>Task Result:</b> {item.task_result}</p>
                                    <p><b>Task Status:</b>{item.task_status}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>

        
    );
}

export default ViewQueues;

