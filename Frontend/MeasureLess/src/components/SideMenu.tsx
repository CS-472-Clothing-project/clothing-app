import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { FaBars, FaHome, FaListUl, FaCamera, FaInfoCircle, FaRulerCombined } from "react-icons/fa";

/**
 * Slide-out drawer shown on top of content.
 * - Header with hamburger button
 * - Overlay darkens page and blocks clicks
 * - Drawer with nav links
 */
export default function SideMenu() {
  const [open, setOpen] = useState(false);
  const loc = useLocation();

  // Prevent body scroll while menu is open (nice touch for mobile)
  useEffect(() => {
    if (open) {
      const prev = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      return () => { document.body.style.overflow = prev; };
    }
  }, [open]);

  const NavItem = ({
    to,
    label,
    icon,
  }: {
    to: string;
    label: string;
    icon: React.ReactNode;
  }) => {
    const active =
      loc.pathname === to || (to !== "/" && loc.pathname.startsWith(to));
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

  return (
    <>
      {/* Top bar */}
      <header className="relative z-30 h-12 md:h-14 w-full flex items-center px-3 md:px-4">
        <button
          aria-label="Open menu"
          className="inline-flex items-center gap-2 rounded-lg border px-3 py-2 hover:opacity-90"
          onClick={() => setOpen(true)}
        >
          <FaBars />
          <span className="hidden md:inline">Menu</span>
        </button>
      </header>

      {/* Overlay (on top of everything except the drawer) */}
      {open && (
        <div
          className="fixed inset-0 bg-black/35 z-40"
          onClick={() => setOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Drawer (highest layer) */}
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
          <NavItem to="/userInput.tsx"  label="User Input"   icon={<FaListUl />} />
          <NavItem to="/takePicture.tsx"label="Take Picture" icon={<FaCamera />} />
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
