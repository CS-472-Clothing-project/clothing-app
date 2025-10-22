// App.tsx
// App router: defines all routes and gives Home a simple landing with the menu.

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import UserInput from './userInput'
import TakePicture from './takePicture.tsx'
import Instructions from './instructions'
import Output from './output.tsx'
import SideMenu from './components/SideMenu'

// Landing page so people have somewhere to start
function Home() {
  return (
    <div className="min-h-screen w-full flex justify-center">
      <main className="w-full max-w-5xl px-4 md:px-8 py-6 md:py-10 space-y-6">
        {/* Reusable hamburger menu at the top */}
        <SideMenu />
        <h1 className="text-2xl md:text-3xl font-bold">Home Page</h1>
        <p className="opacity-70">
          Welcome to the MeasureLess prototype. Use the menu to navigate between pages.
        </p>
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* If you rename files/paths, update routes here */}
        <Route path="/" element={<Home />} />
        <Route path="/userInput.tsx" element={<UserInput />} />
        <Route path="/takePicture.tsx" element={<TakePicture />} />
        <Route path="/instructions" element={<Instructions />} />
        <Route path="/output" element={<Output />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
