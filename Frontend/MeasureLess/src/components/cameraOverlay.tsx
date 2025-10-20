import { useEffect, useRef, useState } from "react";

const CameraOverlay: React.FC = () => {
    const videoRef = useRef<HTMLVideoElement | null>(null); // ref to video
    const canvasRef = useRef(null); // ref to canvas to convert to img
    const [stream, setStream] = useState<MediaStream | null>(null); // MediaStream 
    const [cameraImage, setCameraImage] = useState<string | null>(null); // image
    const [facingMode, setFacingMode] = useState('user'); // front("user")/back("environment") camera state

    // for intial camera and when face change
    useEffect(() => {
        startCamera(); // start camera function on mount or faceChange
        return () => stopCamera(); // stops camera on unmounts 
    }, [facingMode])

    // start camera
    const startCamera = async () => {
        try {
            // uses mediaDevices to use camera
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode, // sets camera face
                    width: { ideal: 720 },
                    height: { ideal: 1280 },
                },
                audio: false
            });
            /* use the stream */
            setStream(mediaStream); // stores stream in state

            // connect stream to video
            if (videoRef.current)
                videoRef.current.srcObject = mediaStream;

        } catch (err) {
            /* handle the error */
            console.log('error initCamera', err)
        }

    }

    // stops camera
    const stopCamera = () => {
        if (stream) { // iterate through stream
            stream.getTracks().forEach(track => track.stop());
            setStream(null); // clears stream
        }
    }
    /*
    // take photo using camera and display it
    const capturePhoto = () => {
        // use video and canvas
        
        // set canvas to match video
        
        // draw video into canvas
        
        // convert canvas to JPEG
        
        // store as base64 URL

        // stop camera
    }

    const sendToBackend = () => {
        // comvert to blob
    }

    retake photo with a button
    const retakePhoto = () => {
       // clear capturedImage state

        // recall startCamera
        startCamera();
    }

    // switch back <-> front camera with button
    const switchCamera = () => {
        //update facingMode state


    }
    */
    // display video camera
    return (
        <div className="relative w-full h-full">
            {/*if theres no camera image..*/}
            {!cameraImage ? (
                <>
                    {/* do video feed */}
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="absolute top-0 left-0 w-full h-full object-cover pointer-events-none rounded-lg"
                    />
                    <button
                        onClick={stopCamera}
                        className="absolute transform -translate-x-1/2 bottom-8 left-1/2 w-16 h-16 rounded-full bg-gray-50
                        border-3 border-gray-300 hover:border-gray-400 z-10"
                    >
                    </button>
                </>
            ) : (
                <>
                    {/* if you took the photo */}
                    <img />
                </>
            )}
        </div>
    )
}
export default CameraOverlay
