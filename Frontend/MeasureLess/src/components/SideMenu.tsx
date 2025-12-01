import { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { FaBars, FaHome, FaListUl, FaCamera, FaInfoCircle, FaRulerCombined, FaUserCircle, FaSignInAlt, FaSignOutAlt, FaHistory } from "react-icons/fa";
import { useAuth } from "../contexts/authContext";
import { doSignOut } from "../firebase/auth";

// Added optional title prop to display in the header
export default function SideMenu({ title }: { title?: string }) {
  const [open, setOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const loc = useLocation();
  const navigate = useNavigate();
  const { currentUser, userLoggedIn } = useAuth();

  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = prev; };
  }, [open]);

  const handleLogout = async () => {
    try {
      await doSignOut();
      navigate("/login");
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  const NavItem = ({ to, label, icon }: { to: string; label: string; icon: React.ReactNode }) => {
    const active = loc.pathname === to || (to !== "/" && loc.pathname.startsWith(to));
    return (
      <Link
        to={to}
        onClick={() => setOpen(false)}
        className={`flex items-center gap-3 px-4 py-3 rounded-lg border mb-2 hover:opacity-90 ${
          active ? "bg-foreground text-background" : "bg-secondary"
        }`}
      >
        <span className="text-lg">{icon}</span>
        <span className="text-sm md:text-base">{label}</span>
      </Link>
    );
  };

  const isGuest = !userLoggedIn || currentUser?.isAnonymous;

  return (
    <>
      {/* GLASSMORPHIC HEADER */}
      <header className="flex items-center justify-between bg-white/30 backdrop-blur-md p-3 rounded-2xl sticky top-2 z-20 shadow-sm border border-white/40 mb-6">
        
        {/* Left: Menu Toggle (White Pill) */}
        <div className="flex items-center gap-3">
            <button
            aria-label="Open menu"
            className="inline-flex items-center gap-2 rounded-full bg-white px-4 py-2 text-gray-700 shadow-sm hover:bg-gray-50 transition-colors font-bold text-sm"
            onClick={() => setOpen(true)}
            >
            <FaBars />
            <span className="hidden md:inline">Menu</span>
            </button>
            
            {/* Optional Title in Header */}
            {title && (
                <h1 className="text-lg font-bold text-gray-800 ml-2">{title}</h1>
            )}
        </div>

        {/* Right: Profile or Login (White Pill) */}
        <div className="relative">
          {isGuest ? (
            <Link 
              to="/login" 
              className="flex items-center gap-2 px-4 py-2 rounded-full bg-white text-indigo-600 font-bold text-sm shadow-sm hover:bg-gray-50 transition-all"
            >
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

              {/* Profile Dropdown */}
              {profileOpen && (
                <>
                  <div className="fixed inset-0 z-40" onClick={() => setProfileOpen(false)}></div>
                  <div className="absolute right-0 top-full mt-2 w-60 bg-white border border-gray-100 rounded-2xl shadow-xl z-50 overflow-hidden ring-1 ring-black/5">
                    <div className="px-5 py-4 border-b bg-gray-50/50">
                      <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Signed in as</p>
                      <p className="text-sm font-semibold text-gray-800 truncate">{currentUser.email}</p>
                    </div>
                    
                    <Link 
                      to="/output" 
                      onClick={() => setProfileOpen(false)}
                      className="flex items-center gap-3 px-5 py-3 hover:bg-gray-50 text-gray-700 transition-colors"
                    >
                      <FaHistory className="text-indigo-500" /> Past Measurements
                    </Link>
                    
                    <button 
                      onClick={handleLogout}
                      className="w-full text-left flex items-center gap-3 px-5 py-3 hover:bg-red-50 text-red-600 border-t border-gray-100 transition-colors"
                    >
                      <FaSignOutAlt /> Sign Out
                    </button>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </header>

      {/* Drawer Overlay */}
      {open && (
        <div
          className="fixed inset-0 bg-black/35 z-40"
          onClick={() => setOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Navigation Drawer */}
      <aside
        className={`fixed top-0 left-0 h-full w-72 max-w-[80vw] bg-card border-r shadow-xl transition-transform z-50 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
        role="dialog"
        aria-label="Navigation menu"
      >
        <div className="h-14 flex items-center px-4 border-b">
          <span className="font-semibold">Navigation</span>
        </div>

        <nav className="p-2">
          <NavItem to="/"               label="Home"         icon={<FaHome />} />
          <NavItem to="/userInput"      label="User Input"   icon={<FaListUl />} />
          <NavItem to="/takePicture"    label="Take Picture" icon={<FaCamera />} />
          <NavItem to="/instructions"   label="Instructions" icon={<FaInfoCircle />} />
          <NavItem to="/output"         label="Measurements" icon={<FaRulerCombined />} />
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t">
          <p className="text-xs opacity-70">AI Tailor • No human review of images</p>
        </div>
      </aside>
    </>
  );
}