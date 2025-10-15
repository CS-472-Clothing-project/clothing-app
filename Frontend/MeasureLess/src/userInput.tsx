import React, { useState } from "react";
//import { FaMale } from "react-icons/fa";
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
                }}
            >Male Icon</button>

            <button
                onClick={() => setBodyType("other")}
                style={{
                    width:"80px",
                    height:"80px",
                    border: "1px solid black",
                }}
            >Other Icon</button>


            <button
                onClick={() => setBodyType("female")}
                style={{
                    width:"80px",
                    height:"80px",
                    border: "1px solid black",
                }}
            >Female Icon</button>



            <p>Current body Type: {bodyType || "not set"}</p>
        </>
    );
}
export default UserInput;