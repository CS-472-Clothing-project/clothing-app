import CameraOverlay from './components/cameraOverlay'
import React from "react";

const TakePicture: React.FC = () => {
    return (
        <div className="flex-1 flex items-start justify-center pt-10 pb-16 px-4">
            <div className="w-full" style={{ maxWidth: '400px' }}>
                <div className='relative'>
                    {/* Card container with rounded corners and shadow */}
                    <div className="rounded-lg shadow-2xl overflow-hidden">
                        {/* aspect ratio, black background, viewport hiegh for video*/}
                        <div className="relative aspect-[9/16] bg-black w-full max-w-[50vh]">
                            <CameraOverlay />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TakePicture;

