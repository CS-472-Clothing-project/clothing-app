// output.tsx
// Measurement results screen.
// - Displays values with In/Cm toggle
// - "Save to profile" stores a snapshot in localStorage (prototype only)
// - "Export to CSV" downloads a simple CSV of the current table

import { useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import SideMenu from "./components/SideMenu";
import { doSaveToProfile, deleteFromProfile, getMeasurementsFromDB } from './firebase/db.js';
import { auth } from './firebase/firebase.js'

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

// Convert inches → centimeters for display
function toCm(inches: number) { return inches * 2.54; }

// Format a numeric value according to unit
function formatValue(v: number | undefined, unit: Unit) {
    if (v == null) return "—";
    const n = unit === "in" ? v : toCm(v);
    const digits = unit === "in" ? 2 : 1;
    return `${n.toFixed(digits)} ${unit}`;
}

// Escape CSV fields if they contain commas/quotes/newlines
function csvEscape(text: string) {
    return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export default function Output() {
    // If the camera page navigated here with data, it will be in location.state
    const user = auth.currentUser;
    const isAnonymous = user?.isAnonymous;

    const location = useLocation() as {
        state?: {
            measurements?: MeasurementPayload,
            height?: number
        }
    };

    // Fallback values so this screen isn't empty
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

    // Merge any incoming values over the fallback
    const measurements: MeasurementPayload = useMemo(
        () => ({
            ...fallback, ...(location.state?.measurements ?? {}),
            height: location.state?.height ?? 0
        }),
        [location.state]
    );

    const [unit, setUnit] = useState<Unit>("in");

    // Build table rows in display order
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

    // Download CSV of the table
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

    // Save into localStorage (prototype-only “profile”)
    function handleSaveProfile() {
        doSaveToProfile(measurements);
    }

    // View prior measurements
    function handlePriorMeasurements() {
        //measurements = getMeasurementsFromDB();
    }

    return (
        <div className="min-h-screen w-full flex justify-center">
            <main className="w-full max-w-5xl px-4 md:px-8 py-6 md:py-10 space-y-6">
                <SideMenu />

                {/* Heading + Unit Toggle */}
                <header className="flex items-center justify-between">
                    <h1 className="text-2xl md:text-3xl font-bold">Measurements</h1>
                    <div className="flex items-center gap-2">
                        <span className="mr-1 text-sm opacity-70">Units:</span>
                        <div className="inline-flex rounded-full border overflow-hidden">
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

                {/* Results table */}
                <section className="w-full border rounded-2xl p-4 md:p-6">
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm md:text-base">
                            <thead>
                                <tr className="text-left">
                                    <th className="pb-2 md:pb-3">Measurement Type</th>
                                    <th className="pb-2 md:pb-3">Result</th>
                                </tr>
                            </thead>
                            <tbody className="align-top">
                                {rows.map((r) => (
                                    <tr key={r.key} className="border-t">
                                        <td className="py-2 md:py-3">{r.label}</td>
                                        <td className="py-2 md:py-3">{formatValue(r.value, unit)}</td>
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
                        onClick={handleSaveProfile} className="px-6 py-2 rounded-full border hover:opacity-90 hover:cursor-pointer">
                        Save to profile
                    </button>
                    <button
                        disabled={isAnonymous}
                        onClick={handlePriorMeasurements} className="px-6 py-2 rounded-full border hover:opacity-90 hover:cursor-pointer">
                        Past Measurements
                    </button>
                    <button onClick={handleExportCSV} className="px-6 py-2 rounded-full border hover:opacity-90 hover:cursor-pointer">
                        Export to CSV
                    </button>
                    <Link to="/TakePicture" className="px-6 py-2 rounded-full border hover:opacity-90 text-center">
                        Retake Photos
                    </Link>
                </div>
            </main>
        </div>
    );
}
