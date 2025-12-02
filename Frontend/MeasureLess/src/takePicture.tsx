import CameraOverlay from './components/cameraOverlay'
import React, { useState } from "react";
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { FaArrowLeft, FaSignInAlt, FaUserCircle, FaHistory, FaSignOutAlt, FaRulerHorizontal } from "react-icons/fa";
import { NewtonsCradle } from 'ldrs/react'
import 'ldrs/react/NewtonsCradle.css'

import { useAuth } from "./contexts/authContext";
import { doSignOut } from "./firebase/auth";

const TakePicture: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const height = location.state?.height;

    const [showOverlay, setShowOverlay] = useState(true);


    // Auth & Profile state
    const { currentUser, userLoggedIn } = useAuth();
    const [profileOpen, setProfileOpen] = useState(false);
    const isGuest = !userLoggedIn || currentUser?.isAnonymous;

    // FIXED: Explicitly go back to Instructions, ensuring height state is passed back
    const handleBack = () => {
        navigate("/instructions", { state: { height: height } });
    };

    const handleLogout = async () => {
        try {
            await doSignOut();
            navigate("/login");
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="min-h-screen w-full flex justify-center bg-[#b4a7d6]">
            <main className="w-full max-w-5xl px-4 md:px-8 py-6 space-y-4">

                {/* GLASSMORPHIC HEADER */}
                <header className="flex items-center justify-between bg-white/30 backdrop-blur-md p-3 rounded-2xl sticky top-2 z-20 shadow-sm border border-white/40 mb-2">
                    <div className="flex items-center">
                        <button
                            onClick={handleBack}
                            className="p-2 rounded-full hover:bg-white/50 transition-colors text-gray-800"
                            aria-label="Go back"
                        >
                            <FaArrowLeft size={20} />
                        </button>
                        <span className="ml-3 font-bold text-gray-800 text-lg">Camera Setup</span>
                    </div>

                    {/* Profile / Login Section */}
                    <div className="relative">
                        {isGuest ? (
                            <Link to="/login" className="flex items-center gap-2 px-4 py-2 rounded-full bg-white text-indigo-600 font-bold text-sm shadow-sm hover:bg-gray-50 transition-all">
                                <span>Login</span>
                                <FaSignInAlt />
                            </Link>
                        ) : (
                            <div>
                                <button
                                    onClick={() => setProfileOpen(!profileOpen)}
                                    className="flex items-center gap-2 px-2 py-1 pl-3 rounded-full bg-white border border-purple-100 shadow-sm hover:shadow-md transition-all"
                                >
                                    <span className="text-xs font-bold text-indigo-900 hidden sm:block max-w-[100px] truncate">
                                        {currentUser?.email?.split('@')[0]}
                                    </span>
                                    <FaUserCircle size={28} className="text-indigo-600" />
                                </button>
                                {profileOpen && (
                                    <>
                                        <div className="fixed inset-0 z-40" onClick={() => setProfileOpen(false)}></div>
                                        <div className="absolute right-0 top-full mt-2 w-64 bg-white border border-gray-100 rounded-2xl shadow-xl z-50 overflow-hidden ring-1 ring-black/5">
                                            <div className="px-5 py-4 border-b bg-gray-50/50">
                                                <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Signed in as</p>
                                                <p className="text-sm font-semibold text-gray-800 truncate">{currentUser.email}</p>
                                            </div>

                                            <Link to="/userInput" className="flex items-center gap-3 px-5 py-3 hover:bg-indigo-50 text-indigo-700 font-semibold transition-colors border-b border-gray-50">
                                                <FaRulerHorizontal /> Get Measured
                                            </Link>

                                            <Link to="/output" className="flex items-center gap-3 px-5 py-3 hover:bg-gray-50 text-gray-700 transition-colors">
                                                <FaHistory className="text-gray-500" /> Past Measurements
                                            </Link>
                                            <button onClick={handleLogout} className="w-full text-left flex items-center gap-3 px-5 py-3 hover:bg-red-50 text-red-600 border-t border-gray-100 transition-colors">
                                                <FaSignOutAlt /> Sign Out
                                            </button>
                                        </div>
                                    </>
                                )}
                            </div>
                        )}
                    </div>
                </header>

                {showOverlay ? (
                    <div className="flex-1 flex items-start justify-center pt-2 pb-8">
                        <div className="w-full" style={{ maxWidth: '400px' }}>
                            <div className='relative'>
                                <div className="rounded-lg shadow-2xl overflow-hidden border-2 border-black bg-black">
                                    <div className="relative aspect-[9/16] bg-black w-full max-w-[50vh]">

                                        <CameraOverlay height={height} onComplete={() => setShowOverlay(false)} />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    // if sending backend, loading!!
                    <div className="flex items-center justify-center w-full h-full text-white cursor-progress animate-pulse">
                        <NewtonsCradle
                            size="200"
                            speed="1.4"
                            color="black"
                        />
                    </div>
                )}            </main>
        </div>
    );
};

export default TakePicture;
