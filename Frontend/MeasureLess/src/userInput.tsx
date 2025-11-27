// userInput.tsx
// Collect body type + height via a simple wheel picker. Then move into the flow.

import { useState } from "react";
import { FaMale, FaFemale, FaUser } from "react-icons/fa";
import "./assets/react.svg";
import Picker from 'react-mobile-picker';
import { useNavigate } from "react-router-dom";
import SideMenu from "./components/SideMenu";

function UserInput() {
    // Track the selected body type (male/female/other)
    const [bodyType, setBodyType] = useState("");
    // Options for the height wheel
    const selections = {
        feet: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        inches: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
    };
    // Controlled value for the wheel
    const [pickerValue, setPickerValue] = useState({ feet: "0", inches: "0" });

    const navigate = useNavigate();


    // For now we just navigate to /instructions; later this can pass data 
    const handleSubmit = () => {
        const heightInches = parseInt(pickerValue.feet) * 12 + parseInt(pickerValue.inches);
        console.log(heightInches)
        navigate("/instructions", {
            state: {
                height: heightInches
            }
        })
    };

    return (
        <div className="min-h-screen w-full flex justify-center">
            <main className="w-full max-w-5xl px-4 md:px-8 py-6 md:py-10 space-y-6">
                {/* Global nav */}
                <SideMenu />

                <h1 className="text-2xl font-semibold text-center mb-2">User Input</h1>

                {/* Body-type selector */}
                <div className="text-center mb-6">
                    <h2 className="text-lg font-semibold mb-4 border-b pb-2">
                        Please Choose Your Body Type
                    </h2>
                    <div className="flex flex-row justify-center items-center gap-8">
                        {/* Male */}
                        <div className="flex flex-col justify-center items-center">
                            <button
                                onClick={() => { setBodyType("male") }}
                                className={`w-36 h-36 border rounded-lg flex justify-center items-center ${bodyType === "male"
                                    ? "border-blue-800 w-40 h-40"
                                    : "border-black hover:border-blue-800 hover:w-40 hover:h-40 hover:cursor-pointer"
                                    }`}
                            >
                                <FaMale size={67} />
                            </button>
                            <h2>Male</h2>
                        </div>

                        {/* Prefer not to say / other */}
                        <div className="flex flex-col justify-center items-center">
                            <button
                                onClick={() => setBodyType("other")}
                                className={`w-36 h-36 border rounded-lg flex justify-center items-center ${bodyType === "other"
                                    ? "border-blue-800 w-40 h-40"
                                    : "border-black hover:border-blue-800 hover:w-40 hover:h-40 hover:cursor-pointer"
                                    }`}
                            >
                                <FaUser size={67} />
                            </button>
                            <h2>Pref not to say</h2>
                        </div>

                        {/* Female */}
                        <div className="flex flex-col justify-center items-center">
                            <button
                                onClick={() => setBodyType("female")}
                                className={`w-36 h-36 border rounded-lg flex justify-center items-center ${bodyType === "female"
                                    ? "border-blue-800 w-40 h-40"
                                    : "border-black hover:border-blue-800 hover:w-40 hover:h-40 hover:cursor-pointer"
                                    }`}
                            >
                                <FaFemale size={67} />
                            </button>
                            <h2>Female</h2>
                        </div>
                    </div>
                </div>

                {/* Height wheel picker */}
                <div className="text-center mb-6">
                    <h2 className="text-lg font-semibold mb-4 border-b pb-2">
                        Please Enter your Height
                    </h2>
                    <div className="flex flex-row justify-center">
                        <div className="bg-gray-100 rounded-xl shadow-lg justify-center items-center w-1/2">
                            <Picker value={pickerValue} onChange={setPickerValue} wheelMode={"normal"}>
                                <Picker.Column name={"feet"}>
                                    {selections.feet.map((ft) => (
                                        <Picker.Item key={ft} value={ft}>
                                            {ft} ft.
                                        </Picker.Item>
                                    ))}
                                </Picker.Column>
                                <Picker.Column name={"inches"}>
                                    {selections.inches.map((inch) => (
                                        <Picker.Item key={inch} value={inch}>
                                            {inch} in.
                                        </Picker.Item>
                                    ))}
                                </Picker.Column>
                            </Picker>
                        </div>
                    </div>
                </div>

                {/* Continue button */}
                <div className="flex justify-center">
                    <button
                        onClick={handleSubmit}
                        disabled={!bodyType || !pickerValue.feet}
                        className={`px-6 py-3 rounded-lg font-medium text-white transition-all ${!bodyType || !pickerValue.feet
                            ? "bg-gray-400 cursor-not-allowed"
                            : "bg-black hover:cursor-pointer shadow"
                            }`}
                    >
                        Submit and Measure
                    </button>
                </div>
            </main>
        </div>
    );
}

export default UserInput;
