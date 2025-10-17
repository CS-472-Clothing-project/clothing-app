import { useState } from "react";
import { FaMale, FaFemale, FaUser } from "react-icons/fa";
import "./assets/react.svg";
import Picker from 'react-mobile-picker';


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

    return(
        <div className="flex flex-col">
            <h1>User Input</h1>

            <div className="flex flex-row justify-around align-items-center">
                <button
                    onClick={() => {setBodyType("male")}}
                    className={`w-36 h-36 border border-black rounded-lg flex justify-center items-center
                        ${
                        bodyType === "male"
                            ? "border-blue-800 w-40 h-40"  //selected
                            : "border-black hover:border-blue-800 hover:w-40 hover:h-40"    // not selected
                    }`}
                ><FaMale size={67}/></button>


                <button
                    onClick={() => setBodyType("other")}
                    className={`w-36 h-36 border border-black rounded-lg flex justify-center items-center
                        ${
                        bodyType === "other"
                            ? "border-blue-800 w-40 h-40"
                            : "border-black hover:border-blue-800 hover:w-40 hover:h-40"
                    }`}
                ><FaUser size={67}/></button>


                <button
                    onClick={() => setBodyType("female")}
                    className={`w-36 h-36 border border-black rounded-lg flex justify-center items-center
                        ${
                        bodyType === "female"
                            ? "border-blue-800 w-40 h-40"
                            : "border-black hover:border-blue-800 hover:w-40 hover:h-40"
                    }`}
                ><FaFemale size={67}/></button>
            </div>


            <p>Current body Type: {bodyType || "not set"}</p>
            <div className="border-black flex justify-center items-center">
            <Picker value={pickerValue} onChange={setPickerValue} wheelMode={"natural"}>
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
            Selected height: <strong>{pickerValue.feet} ft {pickerValue.inches} in</strong>
        </div>
    );
}
export default UserInput;