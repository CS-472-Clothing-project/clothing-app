import { useState } from "react";
import { 
    FaCamera, FaTshirt, FaRulerCombined, FaUserShield, 
    FaMobileAlt, FaAngleDoubleUp, FaArrowLeft, FaSignInAlt, 
    FaUserCircle, FaHistory, FaSignOutAlt, FaCheckCircle, FaLightbulb, FaRulerHorizontal
} from "react-icons/fa";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { useAuth } from "./contexts/authContext";
import { doSignOut } from "./firebase/auth";

export default function Instructions() {
    const navigate = useNavigate();
    const location = useLocation();
    const { currentUser, userLoggedIn } = useAuth();
    const [profileOpen, setProfileOpen] = useState(false);

    // FIXED: Explicitly go back to User Input
    const handleBack = () => navigate("/userInput");

    const handleLogout = async () => {
        try {
            await doSignOut();
            navigate("/login");
        } catch (error) {
            console.error(error);
        }
    };

    const navi = () => {
        navigate("/takePicture", {
            state: {
                height: location.state?.height
            }
        })
    }

    const isGuest = !userLoggedIn || currentUser?.isAnonymous;

    // --- Components ---
    const QuickCard = ({ icon, title, text }: { icon: React.ReactNode, title: string, text: string }) => (
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-purple-50 flex flex-col items-center text-center gap-3 transition-transform hover:scale-[1.02]">
            <div className="text-3xl text-indigo-600 bg-indigo-50 p-3 rounded-full mb-1">
                {icon}
            </div>
            <h3 className="font-bold text-gray-800">{title}</h3>
            <p className="text-sm text-gray-500 leading-relaxed">{text}</p>
        </div>
    );

    const BulletItem = ({ text }: { text: string }) => (
        <li className="flex items-start gap-3 py-1">
            <span className="mt-1 text-indigo-500 shrink-0">
                <FaCheckCircle />
            </span>
            <span className="text-gray-700">{text}</span>
        </li>
    );

    return (
        <div className="min-h-screen w-full flex justify-center bg-[#b4a7d6]">
            <main className="w-full max-w-4xl px-4 md:px-6 py-6 pb-24 space-y-6">
                
                {/* --- Header --- */}
                <header className="flex items-center justify-between bg-white/30 backdrop-blur-md p-3 rounded-2xl sticky top-2 z-20 shadow-sm border border-white/40">
                    <div className="flex items-center">
                        <button 
                            onClick={handleBack}
                            className="p-2 rounded-full hover:bg-white/50 transition-colors text-gray-800"
                            aria-label="Go back"
                        >
                            <FaArrowLeft size={20} />
                        </button>
                        <span className="ml-3 font-bold text-gray-800 text-lg hidden md:inline">Instructions</span>
                    </div>

                    {/* Profile / Login Section */}
                    <div className="relative">
                        {isGuest ? (
                            <Link to="/login" className="flex items-center gap-2 px-4 py-2 rounded-full bg-white text-indigo-600 font-bold text-sm shadow-sm hover:bg-gray-50">
                                <span>Login</span>
                                <FaSignInAlt />
                            </Link>
                        ) : (
                            <div>
                                <button 
                                    onClick={() => setProfileOpen(!profileOpen)}
                                    className="flex items-center gap-2 p-1 pl-3 pr-2 rounded-full bg-white border border-purple-100 shadow-sm hover:shadow-md transition-all"
                                >
                                    <span className="text-xs font-bold text-indigo-900 hidden sm:block max-w-[100px] truncate">
                                        {currentUser?.email?.split('@')[0]}
                                    </span>
                                    <FaUserCircle size={28} className="text-indigo-600" />
                                </button>
                                {profileOpen && (
                                    <>
                                        <div className="fixed inset-0 z-40" onClick={() => setProfileOpen(false)}></div>
                                        <div className="absolute right-0 top-full mt-3 w-64 bg-white border border-gray-100 rounded-2xl shadow-xl z-50 overflow-hidden ring-1 ring-black/5">
                                             <div className="px-5 py-4 border-b bg-gray-50/50">
                                                <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Signed in as</p>
                                                <p className="text-sm font-semibold text-gray-800 truncate">{currentUser?.email}</p>
                                            </div>
                                            
                                            <Link to="/userInput" className="flex items-center gap-3 px-5 py-3 hover:bg-indigo-50 text-indigo-700 font-semibold transition-colors border-b border-gray-50">
                                                <FaRulerHorizontal /> Get Measured
                                            </Link>

                                            <Link to="/output" className="flex items-center gap-3 px-5 py-3 hover:bg-gray-50 text-gray-700 transition-colors">
                                                <FaHistory className="text-gray-500" /> Past Measurements
                                            </Link>
                                            
                                            <button onClick={handleLogout} className="w-full text-left flex items-center gap-3 px-5 py-3 hover:bg-red-50 text-red-600 transition-colors border-t border-gray-100">
                                                <FaSignOutAlt /> Sign Out
                                            </button>
                                        </div>
                                    </>
                                )}
                            </div>
                        )}
                    </div>
                </header>

                <div className="space-y-1">
                    <h1 className="text-3xl md:text-4xl font-black text-gray-900 text-center md:text-left mt-4">
                        Let's Get Set Up
                    </h1>
                    <p className="text-gray-700 font-medium text-center md:text-left opacity-80">
                        Follow these steps for accurate AI measurements.
                    </p>
                </div>

                {/* --- Quick Visual Tips --- */}
                <section className="grid md:grid-cols-3 gap-4">
                    <QuickCard 
                        icon={<FaMobileAlt />} 
                        title="Position Phone" 
                        text="Place on a stable surface (desk/table) at waist height. Vertical & 90° straight." 
                    />
                    <QuickCard 
                        icon={<FaTshirt />} 
                        title="Tight Clothing" 
                        text="Wear form-fitting clothes. Tuck in shirts. Avoid baggy jackets or dresses." 
                    />
                    <QuickCard 
                        icon={<FaRulerCombined />} 
                        title="Distance" 
                        text="Stand 6-8 feet back. Ensure your head and feet are fully visible in the frame." 
                    />
                </section>

                <div className="grid md:grid-cols-2 gap-6">
                    {/* --- Environment & Clothing Details --- */}
                    <div className="space-y-4">
                         <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-sm">
                            <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-gray-800">
                                <FaLightbulb className="text-yellow-500" /> Environment
                            </h2>
                            <ul className="space-y-2 text-sm md:text-base">
                                <BulletItem text="Plain background (door or wall) works best." />
                                <BulletItem text="Use even lighting; avoid dark shadows." />
                                <BulletItem text="Remove clutter from the floor around you." />
                            </ul>
                        </div>

                        <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-sm">
                            <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-gray-800">
                                <FaUserShield className="text-green-500" /> Privacy First
                            </h2>
                            <p className="text-sm text-gray-600 leading-relaxed">
                                Your photos are processed instantly by our AI server and are <strong>never seen by humans</strong>. 
                                We only extract measurement data points.
                            </p>
                        </div>
                    </div>

                    {/* --- Checklist --- */}
                    <div className="bg-indigo-900 text-white p-6 md:p-8 rounded-2xl shadow-lg flex flex-col justify-between">
                        <div>
                            <h2 className="text-2xl font-bold mb-6">Ready to Start?</h2>
                            <ol className="space-y-4">
                                <li className="flex gap-4">
                                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-white/20 font-bold shrink-0">1</span>
                                    <p className="mt-1 opacity-90">Prop phone vertically against a stable object.</p>
                                </li>
                                <li className="flex gap-4">
                                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-white/20 font-bold shrink-0">2</span>
                                    <p className="mt-1 opacity-90">Step back 6-8 feet until your full body fits.</p>
                                </li>
                                <li className="flex gap-4">
                                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-white/20 font-bold shrink-0">3</span>
                                    <p className="mt-1 opacity-90">Relax arms, look straight, and wait for the timer.</p>
                                </li>
                            </ol>
                        </div>
                        
                        <div className="hidden md:block mt-8">
                             <button onClick={navi}
                                className="w-full py-4 rounded-xl bg-white text-indigo-900 font-bold text-lg hover:bg-gray-100 transition-colors shadow-lg flex items-center justify-center gap-2">
                                <FaCamera /> Open Camera
                            </button>
                        </div>
                    </div>
                </div>

                {/* --- Mobile Sticky Button --- */}
                <div className="md:hidden fixed bottom-6 left-4 right-4 z-30">
                     <button onClick={navi}
                        className="w-full py-4 rounded-xl bg-black text-white font-bold text-lg shadow-2xl flex items-center justify-center gap-2 border border-gray-700 active:scale-95 transition-transform">
                        <FaCamera /> Open Camera
                    </button>
                </div>

            </main>
        </div>
    );
}