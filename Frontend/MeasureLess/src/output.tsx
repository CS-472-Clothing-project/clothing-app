// output.tsx
// Measurement results screen.
// - Displays values with In/Cm toggle
// - "Save to profile" stores a snapshot in localStorage (prototype only)
// - "Export to CSV" downloads a simple CSV of the current table

import { useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import SideMenu from "./components/SideMenu";

export type MeasurementPayload = Partial<{
  shoulderWidth: number;
  chest: number;
  waist: number;
  hip: number;
  sleeveLength: number;
  inseam: number;
  outseam: number;
  height: number;
}>;

type Unit = "in" | "cm";

const LABELS: Record<keyof NonNullable<MeasurementPayload>, string> = {
  shoulderWidth: "Shoulder Width",
  chest: "Chest",
  waist: "Waist",
  hip: "Hip",
  sleeveLength: "Sleeve Length",
  inseam: "Inseam",
  outseam: "Outseam",
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
  const location = useLocation() as { state?: { measurements?: MeasurementPayload } };

  // Fallback values so this screen isn't empty
  const fallback: MeasurementPayload = {
    shoulderWidth: 18.0,
    chest: 40.0,
    waist: 35.0,
    hip: 38.0,
    sleeveLength: 24.5,
    inseam: 30.0,
    outseam: 40.0,
  };

  // Merge any incoming values over the fallback
  const measurements: MeasurementPayload = useMemo(
    () => ({ ...fallback, ...(location.state?.measurements ?? {}) }),
    [location.state]
  );

  const [unit, setUnit] = useState<Unit>("in");

  // Build table rows in display order
  const rows = useMemo(
    () =>
      ([
        "shoulderWidth",
        "chest",
        "waist",
        "hip",
        "sleeveLength",
        "inseam",
        "outseam",
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
    const key = "measureless.profiles";
    const existing = JSON.parse(localStorage.getItem(key) || "[]") as any[];
    existing.push({ savedAt: new Date().toISOString(), unit, measurements });
    localStorage.setItem(key, JSON.stringify(existing));
    alert("Saved to profile (local storage).");
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
                className={`px-3 py-1 text-sm ${unit === "in" ? "bg-foreground text-background" : ""}`}
                onClick={() => setUnit("in")}
              >
                In.
              </button>
              <button
                className={`px-3 py-1 text-sm ${unit === "cm" ? "bg-foreground text-background" : ""}`}
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
          <button onClick={handleSaveProfile} className="px-6 py-2 rounded-full border hover:opacity-90">
            Save to profile
          </button>
          <button onClick={handleExportCSV} className="px-6 py-2 rounded-full border hover:opacity-90">
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
