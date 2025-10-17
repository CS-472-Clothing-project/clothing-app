import CameraOverlay from './components/cameraOverlay'
import React from "react";

const TakePicture: React.FC = () => {
    return (
        <div>
            <h1>Take Picture Page</h1>
            {/* Add your camera logic here */}
            <CameraOverlay />
        </div>
    );
};

export default TakePicture;

