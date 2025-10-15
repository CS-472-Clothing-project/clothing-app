import React, { useState } from "react";
import { FaMale, FaFemale, FaUser } from "react-icons/fa";
import "./assets/react.svg";


function UserInput() {
    const[bodyType, setBodyType] = useState("");
    return(
        <>
            <h1>User Input</h1>
            <button
                onClick={() => setBodyType("male")}
                style={{
                    width:"80px",
                    height:"80px",
                    border: "1px solid black",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            ><FaMale size={32}/></button>


            <button
                onClick={() => setBodyType("other")}
                style={{
                    width:"80px",
                    height:"80px",
                    border: "1px solid black",
                }}
            ><FaUser size={32}/></button>


            <button
                onClick={() => setBodyType("female")}
                style={{
                    width:"80px",
                    height:"80px",
                    border: "1px solid black",
                }}
            ><FaFemale size={32}/></button>



            <p>Current body Type: {bodyType || "not set"}</p>
        </>
    );
}
export default UserInput;