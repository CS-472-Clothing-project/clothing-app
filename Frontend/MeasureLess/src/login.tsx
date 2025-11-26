import React, { useState } from 'react';
import { doSignInWithGoogle, doSignInWithEmailAndPassword, doSignInAnonymously } from './firebase/auth.js'
//import { useAuth } from './contexts/authContext/index.jsx'
import { useNavigate } from 'react-router-dom'
import { FcGoogle } from "react-icons/fc";


const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSigningIn, setIsSignIn] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if(!isSigningIn){
            setIsSignIn(true);
            await doSignInWithEmailAndPassword(email, password);
            navigate("/userInput");
        }
    };
    const onGuestLogin = async (e) => {
        e.preventDefault();
        if(!isSigningIn){
            setIsSignIn(true);
            await doSignInAnonymously();
            navigate("/userInput");
        }
    };

    const onGoogleSigIn = async (e) =>{
        e.preventDefault();
        if(!isSigningIn){
            setIsSignIn(true);
            doSignInWithGoogle().catch(err =>{
                setIsSignIn(false);
            });
            navigate("/userInput");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
                <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">Login to your account</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-6">
                        <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                            placeholder="********"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="flex items-center justify-between">
                        <button
                            type="submit"
                            className="bg-purple-300 hover:bg-purple-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                        >
                            Sign In
                        </button>
                    </div>
                </form>
                <div className="mt-4">
                    <button
                        onClick={onGoogleSigIn}
                        disabled={isSigningIn}
                        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full disabled:opacity-50 flex items-center justify-center gap-2"
                    >
                        {isSigningIn ? 'Signing In...' : <><FcGoogle/>Sign in with Google</>}
                    </button>
                </div>
                <div className="mt-4">
                    <button
                        onClick={onGuestLogin}
                        disabled={isSigningIn}
                        className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full disabled:opacity-50"
                    >
                        {isSigningIn ? 'Signing In...' : 'Continue as Guest'}
                    </button>
                </div>
                <div className="mt-4 ">
                    Don't have an account?{" "}
                    <a href="/register" className="text-black font-bold focus:shadow-outline">
                        Sign up
                    </a>
                </div>
            </div>
        </div>
    );
};

export default LoginForm;
