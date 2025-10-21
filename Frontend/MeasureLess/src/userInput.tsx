import { useState } from "react";
import { FaMale, FaFemale, FaUser } from "react-icons/fa";
import "./assets/react.svg";
import Picker from 'react-mobile-picker';
import { useNavigate } from "react-router-dom";


function UserInput() {
    const[bodyType, setBodyType] = useState("");
    //const[userFt, setUserFt] = useState("");
    //const[userIn, setUserIn] = useState("");
    const selections = {
        feet: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        inches: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
    }
    const [pickerValue, setPickerValue] = useState({
        feet: "",
        inches: "",
    });

    const navigate = useNavigate();
    const handleSubmit = () => {
        // TODO: take data and send to server
        // Then navigate to Instructions page
        navigate("/instructions");
    };

    return(
        <div className="flex flex-col">
            <h1 className="text-2xl font-semibold text-center mb-8 text-black">
                User Input
            </h1>


            <div className="text-center mb-10">
            <h2 className="text-lg font-semibold mb-6 text-gray-800 border-b pb-2">
                Please Choose Your Body Type
            </h2>
            <div className="flex flex-row justify-center items-center gap-8">
                <div className="flex flex-col justify-center items-center">
                <button
                    onClick={() => {setBodyType("male")}}
                    className={`w-36 h-36 border border-black rounded-lg flex justify-center items-center
                        ${
                        bodyType === "male"
                            ? "border-blue-800 w-40 h-40"  //selected
                            : "border-black hover:border-blue-800 hover:w-40 hover:h-40 hover:cursor-pointer "    // not selected
                    }`}
                ><FaMale size={67}/></button>
                    <h2>Male</h2>
                </div>

                <div className="flex flex-col justify-center items-center">
                <button
                    onClick={() => setBodyType("other")}
                    className={`w-36 h-36 border border-black rounded-lg flex justify-center items-center
                        ${
                        bodyType === "other"
                            ? "border-blue-800 w-40 h-40"
                            : "border-black hover:border-blue-800 hover:w-40 hover:h-40 hover:cursor-pointer "
                    }`}
                ><FaUser size={67}/></button>
                    <h2>Pref not to say</h2>
                </div>

                <div className="flex flex-col justify-center items-center">
                <button
                    onClick={() => setBodyType("female")}
                    className={`w-36 h-36 border border-black rounded-lg flex justify-center items-center
                        ${
                        bodyType === "female"
                            ? "border-blue-800 w-40 h-40"
                            : "border-black hover:border-blue-800 hover:w-40 hover:h-40 hover:cursor-pointer "
                    }`}
                ><FaFemale size={67}/></button>
                    <h2>Female</h2>
                </div>
            </div>
            </div>



            <div className="text-center mb-10">
                <h2 className="text-lg font-semibold mb-6 text-gray-800 border-b pb-2">
                    Please Enter your Height
                </h2>
                <div className="flex flex-row justify-center align-items-center">
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

            <div className="flex justify-center">
                <button
                    onClick={handleSubmit}
                    disabled={!bodyType || !pickerValue.feet}
                    className={`px-6 py-3 rounded-lg font-medium text-white transition-all ${
                        !bodyType || !pickerValue.feet
                            ? "bg-gray-400 cursor-not-allowed"
                            : "bg-black hover:cursor-pointer shadow"
                    }`}
                >
                    Submit and Measure
                </button>
            </div>
        </div>
    );
}
export default UserInput;