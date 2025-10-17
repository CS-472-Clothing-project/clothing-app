import { useEffect, useRef, useState } from "react";

const cameraOverlay = () => {
    const videoRef = useRef(null); // ref to video
    const canvasRef = useRef(null); // ref to canvas to convert to img
    const [stream, setStream] = useState(false); // MediaStream 
    const [cameraImage, setCameraImage] = useState(null); // image
    const [facingMode, setFacingMode] = useState('user'); // front("user")/back("environment") camera state

    useEffect(() => {
        startCamera(); // start camera function on mount or faceChange
        return () => stopCamera(); // stops camera on unmounts 
    }, [facingMode])

    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode
                },
                audio: false
            });
            /* use the stream */
            setStream(mediaStream);

            if (videoRef.current)
                videoRef.current.srcObject = mediaStream;

        } catch (err) {
            /* handle the error */
            console.log('error initCamera', err)
        }

    }

    /*
    const stopCamera = () => {

    }

    const capturePhoto = () => {

    }

    const sendToBackend = () => {

    }

    const retakePhoto = () => {

    }

    const switchCamera = () => {

    }
    */

}
export default cameraOverlay
