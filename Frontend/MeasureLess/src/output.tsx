// output.tsx
import { useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import SideMenu from "./components/SideMenu";
import { doSaveToProfile, deleteFromProfile, getMeasurementsFromDB } from './firebase/db.js';
import { auth } from './firebase/firebase.js'
import { FaTshirt, FaRunning, FaCity } from "react-icons/fa"; // Icons for vibes

export type MeasurementPayload = Partial<{
    shoulder: number,
    chest: number,
    length: number,
    short_sleeve: number,
    long_sleeve: number,
    hip: number,
    waist: number,
    outseam: number,
    inseam: number,
    height: number,
}>;

type Unit = "in" | "cm";

// --- START SIZE SUGGESTOR LOGIC ---

type FitVibe = "slim" | "regular" | "baggy";

const VIBES: { id: FitVibe; label: string; icon: React.ReactNode; desc: string }[] = [
    { id: "slim", label: "The Sharp Look", icon: <FaTshirt />, desc: "Form-fitting. Best for suits & date nights." },
    { id: "regular", label: "Classic Daily", icon: <FaRunning />, desc: "Comfortable room. Best for office & casual." },
    { id: "baggy", label: "Street / Oversized", icon: <FaCity />, desc: "Loose & relaxed. Best for hoodies & streetwear." },
];

// Simple heuristic: Chest size in inches -> Letter size
// This is a generic estimation for demo purposes
function estimateSize(chestInches: number, vibe: FitVibe): string {
    let size = "";
    // Base standard sizing (Chest)
    if (chestInches < 36) size = "XS";
    else if (chestInches < 38) size = "S";
    else if (chestInches < 41) size = "M";
    else if (chestInches < 44) size = "L";
    else if (chestInches < 48) size = "XL";
    else size = "XXL";

    // Vibe adjustment
    if (vibe === "slim") {
        // If they want slim, stick to true size or maybe suggest "Tailored [Size]"
        return `${size} (Slim Fit)`;
    } else if (vibe === "baggy") {
        // If they want baggy, usually size up one
        const sizes = ["XS", "S", "M", "L", "XL", "XXL", "3XL"];
        const idx = sizes.indexOf(size);
        const upSize = idx >= 0 && idx < sizes.length - 1 ? sizes[idx + 1] : size;
        return `${upSize} (Oversized)`;
    }
    return size; // Regular
}

// --- END SIZE SUGGESTOR LOGIC ---


const LABELS: Record<keyof NonNullable<MeasurementPayload>, string> = {
    shoulder: "Shoulder width",
    chest: "Chest",
    length: "Torso length",
    short_sleeve: "Short Sleeve",
    long_sleeve: "Long Sleeve",
    hip: "Hip",
    waist: "Waist",
    outseam: "Outseam",
    inseam: "Inseam",
    height: "Height",
};

function toCm(inches: number) { return inches * 2.54; }

function formatValue(v: number | undefined, unit: Unit) {
    if (v == null) return "—";
    const n = unit === "in" ? v : toCm(v);
    const digits = unit === "in" ? 2 : 1;
    return `${n.toFixed(digits)} ${unit}`;
}

function csvEscape(text: string) {
    return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export default function Output() {
    const user = auth.currentUser;
    const isAnonymous = user?.isAnonymous;

    const location = useLocation() as {
        state?: {
            measurements?: MeasurementPayload,
            height?: number
        }
    };

    const fallback: MeasurementPayload = {
        height: 0,
        shoulder: 0,
        chest: 0,
        length: 0,
        short_sleeve: 0,
        long_sleeve: 0,
        hip: 0,
        waist: 0,
        outseam: 0,
        inseam: 0,
    };

    const measurements: MeasurementPayload = useMemo(
        () => ({
            ...fallback, ...(location.state?.measurements ?? {}),
            height: location.state?.height ?? 0
        }),
        [location.state]
    );

    const [unit, setUnit] = useState<Unit>("in");
    
    // Size suggestor state
    const [selectedVibe, setSelectedVibe] = useState<FitVibe>("regular");

    const rows = useMemo(
        () =>
            ([
                "shoulder",
                "chest",
                "length",
                "short_sleeve",
                "long_sleeve",
                "hip",
                "waist",
                "outseam",
                "inseam",
                "height",
            ] as (keyof MeasurementPayload)[]).map((key) => ({
                key,
                label: LABELS[key],
                value: measurements[key],
            })),
        [measurements]
    );

    function handleExportCSV() {
        const header = ["Measurement", unit === "in" ? "Value (in)" : "Value (cm)"];
        const lines = [header.join(",")];
        rows.forEach((r) => {
            const val =
                r.value == null
                    ? ""
                    : unit === "in"
                        ? r.value.toFixed(2)
                        : toCm(r.value).toFixed(1);
            lines.push([csvEscape(r.label), csvEscape(val)].join(","));
        });
        const csv = lines.join("\n");
        const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        const stamp = new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-");
        a.download = `measurements-${unit}-${stamp}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }

    function handleSaveProfile() {
        doSaveToProfile(measurements);
    }

    function handlePriorMeasurements() {
        //measurements = getMeasurementsFromDB();
    }

    return (
        <div className="min-h-screen w-full flex justify-center bg-[#b4a7d6]">
            <main className="w-full max-w-5xl px-4 md:px-8 py-6 md:py-10 space-y-6">
                
                {/* Global nav - Only shown on UserInput & Output */}
                <SideMenu />

                <header className="flex items-center justify-between">
                    <h1 className="text-2xl md:text-3xl font-bold">Your Fit Profile</h1>
                    <div className="flex items-center gap-2">
                        <span className="mr-1 text-sm opacity-70">Units:</span>
                        <div className="inline-flex rounded-full border overflow-hidden bg-white shadow-sm">
                            <button
                                className={`px-3 py-1 text-sm hover:cursor-pointer ${unit === "in" ? "bg-foreground text-background" : ""}`}
                                onClick={() => setUnit("in")}
                            >
                                In.
                            </button>
                            <button
                                className={`px-3 py-1 text-sm hover:cursor-pointer ${unit === "cm" ? "bg-foreground text-background" : ""}`}
                                onClick={() => setUnit("cm")}
                            >
                                Cm.
                            </button>
                        </div>
                    </div>
                </header>

                {/* --- SIZE SUGGESTOR SECTION --- */}
                <section className="w-full bg-white rounded-2xl p-6 shadow-md border-2 border-indigo-50">
                    <h2 className="text-xl font-bold mb-4">AI Size Recommendation</h2>
                    
                    {/* Vibe Selection Tabs */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
                        {VIBES.map((v) => (
                            <button
                                key={v.id}
                                onClick={() => setSelectedVibe(v.id)}
                                className={`flex flex-col items-center p-3 rounded-xl border-2 transition-all ${
                                    selectedVibe === v.id 
                                    ? "border-indigo-600 bg-indigo-50 text-indigo-900 shadow-sm" 
                                    : "border-gray-200 hover:border-indigo-300 hover:bg-gray-50 text-gray-600"
                                }`}
                            >
                                <span className="text-2xl mb-1">{v.icon}</span>
                                <span className="font-semibold">{v.label}</span>
                                <span className="text-xs text-center opacity-70 mt-1">{v.desc}</span>
                            </button>
                        ))}
                    </div>

                    {/* The Result Card */}
                    <div className="flex flex-col items-center justify-center p-6 bg-black text-white rounded-xl text-center">
                        <div className="text-sm uppercase tracking-widest opacity-80 mb-1">Your Recommended Size</div>
                        <div className="text-5xl font-black tracking-tight mb-2">
                            {estimateSize(measurements.chest || 0, selectedVibe)}
                        </div>
                        <p className="text-sm opacity-70 max-w-md">
                            Based on your chest measurement of {formatValue(measurements.chest, unit)} and your preference for a 
                            <span className="font-bold text-white"> {VIBES.find(v => v.id === selectedVibe)?.label}</span>.
                        </p>
                    </div>
                </section>
                {/* --- END SIZE SUGGESTOR --- */}

                {/* Results table */}
                <section className="w-full border rounded-2xl p-4 md:p-6 bg-white shadow-md">
                    <h3 className="font-semibold text-lg mb-4">Detailed Measurements</h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm md:text-base">
                            <thead>
                                <tr className="text-left border-b">
                                    <th className="pb-2 text-gray-500 font-medium">Measurement Type</th>
                                    <th className="pb-2 text-gray-500 font-medium">Result</th>
                                </tr>
                            </thead>
                            <tbody className="align-top">
                                {rows.map((r) => (
                                    <tr key={r.key} className="border-b last:border-0 hover:bg-gray-50 transition-colors">
                                        <td className="py-3 font-medium">{r.label}</td>
                                        <td className="py-3 font-mono text-black">{formatValue(r.value, unit)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* Page actions */}
                <div className="flex flex-col md:flex-row gap-3 md:gap-4 md:justify-center">
                    <button
                        disabled={isAnonymous}
                        onClick={handleSaveProfile} className="shadow-xl px-6 py-2 rounded-full border hover:opacity-90 hover:cursor-pointer bg-white">
                        Save to profile
                    </button>
                    <button
                        disabled={isAnonymous}
                        onClick={handlePriorMeasurements} className="shadow-xl px-6 py-2 rounded-full border hover:opacity-90 hover:cursor-pointer bg-white">
                        Past Measurements
                    </button>
                    <button onClick={handleExportCSV} className="shadow-xl px-6 py-2 rounded-full border hover:opacity-90 hover:cursor-pointer bg-white">
                        Export to CSV
                    </button>
                    <Link to="/TakePicture" className="shadow-xl px-6 py-2 rounded-full border hover:opacity-90 text-center bg-white">
                        Retake Photos
                    </Link>
                </div>
            </main>
        </div>
    );
}