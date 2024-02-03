import * as React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [res, setRes] = useState(null);

    const navigate = useNavigate();

    const handleLogin = async () => {
        console.log("Login button clicked");
        let data = {
            email: email,
            password: password,
        }
        console.log("Data:", data);
        try {
            const res = await axios.post("http://" + window.location.hostname + ":8000/login", data);
            console.log(res);
            setRes(res);
            if (res.status === 200) {
                window.alert("Login successful!");
                navigate('/home');
            }
        }
        catch (err) {
            console.log(err.response);
            window.alert("Login failed. Please try again.");
            window.location.href = '/login';
        }

    }

    const handleSignup = async () => {
        console.log("Signup button clicked");
        let data = {
            email: email,
            password: password,
        }
        console.log("Data:", data);
        try {
            const res = await axios.post("http://" + window.location.hostname + ":8000/signup", data);
            console.log(res);
            setRes(res);
            if (res.status === 200) {
                window.alert("Signup successful!");
                navigate('/home');
            }
        }
        catch (err) {
            console.log(err.response);
            window.alert("Signup failed. Please try again.");
            window.location.href = '/login';
        }

    }

    return (
        <div>
            <div className="login">
                <h1>Login</h1>
                <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
                <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
                <button onClick={handleLogin}>Login</button>
            </div>
        </div>
    );
}

export default Login;
