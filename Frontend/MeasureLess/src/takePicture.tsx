// takePicture.tsx
// Hosts the CameraOverlay component inside a 9:16 frame to mimic a phone.
// We keep this page slim so the overlay can focus on camera logic.

import CameraOverlay from './components/cameraOverlay'
import React from "react";
import SideMenu from "./components/SideMenu.tsx";

const TakePicture: React.FC = () => {
  return (
    <div className="min-h-screen w-full flex justify-center">
      <main className="w-full max-w-5xl px-4 md:px-8 py-6 md:py-10 space-y-6">
        <SideMenu />

        <div className="flex-1 flex items-start justify-center pt-2 pb-8">
          <div className="w-full" style={{ maxWidth: '400px' }}>
            <div className='relative'>
              <div className="rounded-lg shadow-2xl overflow-hidden">
                <div className="relative aspect-[9/16] bg-black w-full max-w-[50vh]">
                  <CameraOverlay />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default TakePicture;
