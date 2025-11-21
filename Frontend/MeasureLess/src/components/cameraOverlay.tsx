import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CameraOverlay() {
    const videoRef = useRef<HTMLVideoElement | null>(null); // ref to video
    const canvasRef = useRef<HTMLCanvasElement | null>(null); // ref to canvas to convert to img
    const [stream, setStream] = useState<MediaStream | null>(null); // MediaStream 

    const [frontBlob, setFrontBlob] = useState<Blob | null>(null); // front blob for sending
    const [frontUrl, setFrontUrl] = useState<string | null>(null); // front url for displaying

    const [sideBlob, setSideBlob] = useState<Blob | null>(null) // side blob for sending
    const [sideUrl, setSideUrl] = useState<string | null>(null) // side url for displaying

    const [countdown, setCountDown] = useState<'no-timer' | 'counting'>('no-timer'); // countdown
    const [prevTime, setPrevTime] = useState<number | null>(null);

    const [facingMode, setFacingMode] = useState('user'); // front("user")/back("environment") camera state
    const [photoType, setPhotoType] = useState<'front' | 'side'>('front');

    // for intial camera and when face change
    useEffect(() => {
        startCamera(); // start camera function on mount or faceChange
        return () => stopCamera(); // stops camera on unmounts 
    }, [facingMode])

    useEffect(() => { // countdown
        if (countdown !== 'counting') return;

        console.log("counting");

        setPrevTime(10); // 10 sec countdown

        let timer = setInterval(() => {
            setPrevTime((prevTime) => {
                if (prevTime === null) return null;
                if (prevTime === 0) {
                    clearInterval(timer);
                    setCountDown('no-timer');
                    capturePhoto()
                    return 0;
                }
                return prevTime - 1;
            });
        }, 1000) // 10 seconds delay

        return () => clearInterval((timer));

    }, [countdown])

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

    // take photo using camera and display it
    const capturePhoto = () => {
        // use video and canvas
        const video = videoRef.current
        const canvas = canvasRef.current
        // set canvas to match video
        if (video && canvas) { // if both exist
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            const context = canvas.getContext('2d')
            if (!context) { // debug
                console.log('Could not get canvas context');
                return;
            } else {
                context.drawImage(video, 0, 0);
            }

            // draw video into blob
            canvas.toBlob((blob) => {
                if (!blob) return;

                // Create URL for preview
                const url = URL.createObjectURL(blob);

                if (photoType === 'front') {
                    setFrontBlob(blob);
                    setFrontUrl(url);
                } else if (photoType === 'side') {
                    setSideBlob(blob);
                    setSideUrl(url);
                }
            }, "image/jpeg", 0.95); // 0.95 = 95% quality
        }
    }


    const sendToBackend = async () => {
        let navigate = useNavigate();
        try {
            if (!frontBlob || !sideBlob) {
                console.error("Need both images");
                return;
            }
            // create formData -> append information
            const formData = new FormData();
            formData.append("height", "160");
            formData.append("bodyType", "male");
            // append blob
            formData.append("frontImage", frontBlob, "front.jpg")
            formData.append("sideImage", sideBlob, "side.jpg")
            // post request
            const response = await fetch("http://localhost:5000/api/measure", { //figure out port
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            console.log("Measurements received:", data);

            // go to output 
            navigate('/output', {
                state: { measurements: data }
            });
        } catch (err) {
            console.error("Error POST request with images and info", err);
        }
    }
    /*
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
            <canvas ref={canvasRef} className="hidden" />
            {/*if theres no camera image..*/}
            {!frontUrl ? (
                <>
                    {/* do video feed */}
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        controls={false}
                        className="absolute top-0 left-0 w-full h-full object-cover pointer-events-none rounded-lg
                            [&::-webkit-media-controls]:hidden 
                            [&::-webkit-media-controls-enclosure]:hidden"
                    />
                    {(countdown === 'counting' && prevTime != null) ? (
                        <div className="absolute text-white font-bold text-6xl m-4">
                            {prevTime}
                        </div>
                    ) :
                        (
                            <button
                                onClick={() => {
                                    setPhotoType('front');
                                    setCountDown('counting');
                                }}
                                className="absolute transform -translate-x-1/2 bottom-8 left-1/2 w-16 h-16 rounded-full bg-gray-50
                        border-3 border-gray-300 hover:border-gray-400 z-10"
                            >
                            </button>
                        )}
                </>
            ) : (
                <>
                    {/* if you took the photo */}
                    <img src={frontUrl}
                        alt="captured image"
                        className="absolute top-0 left-0 w-full h-full object-cover"
                    />
                </>
            )}
        </div>
    )
}

