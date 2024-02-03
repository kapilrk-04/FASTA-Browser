import * as React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';


function Homepg() {
    const navigate = useNavigate();

    const titleBarStyle = {
        backgroundColor: ' #333',
        color: '#fff',
        padding: '10px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    };

    const buttonContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', // Make the container full height
    };

    const buttonStyle = {
        backgroundColor: '#007BFF',
        color: '#fff',
        border: 'none',
        padding: '16px 32px', // Increase padding for larger buttons
        borderRadius: '4px',
        cursor: 'pointer',
        margin: '10px', // Add margin between buttons
    };
    
    useEffect(() => {
        navigate('/home');
    }, [navigate]);
    
    return (
        <div>
            <div style={titleBarStyle} className="title-bar">
            <h1>Home</h1>
            </div>

            <div style={buttonContainerStyle} className="home-page">
            <button style={buttonStyle} onClick={() => navigate('/blast_search')}>Perform BLAST Search</button>
            <button style={buttonStyle} onClick={() => navigate('/compare')}>Compare 2 genomes</button>
            <button style={buttonStyle} onClick={() => navigate('/multiple_align')}>Align multiple sequences</button>
            <button style={buttonStyle} onClick={() => navigate('/generate_tree')}>Generate phylogenetic tree</button>
            <button style={buttonStyle} onClick={() => navigate('/variation_analyzer')}>Variation analyzer</button>
            <button style={buttonStyle} onClick={() => navigate('/view_queues')}>View queue logs</button>
            </div>
        </div>
    );
}

export default Homepg;