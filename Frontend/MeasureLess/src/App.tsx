// App.tsx
// App router: defines all routes and gives Home a simple landing with the menu.

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import UserInput from './userInput'
import TakePicture from './takePicture.tsx'
import Instructions from './instructions'
import Output from './output.tsx'
import SideMenu from './components/SideMenu'
import Login from './login'
import { AuthProvider, useAuth } from './contexts/authContext/index.jsx'

// Protected Route component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { userLoggedIn, loading } = useAuth()

  if (loading) {
    return (
        <div className="min-h-screen flex items-center justify-center">
          <div>Loading...</div>
        </div>
    )
  }
  // if not logged cannot access
  return userLoggedIn ? <>{children}</> : <Navigate to="/login" />
}

// User already logged in
function LoggedInRoute({ children }: { children: React.ReactNode }) {
  const { userLoggedIn, loading } = useAuth()

  if (loading) {
    return (
        <div className="min-h-screen flex items-center justify-center">
          <div>Loading...</div>
        </div>
    )
  }
  // if logged in cannot access (such as login page)
  return !userLoggedIn ? <>{children}</> : <Navigate to="/login" />
}

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

function AppContent() {
  return (
    <BrowserRouter>
      <Routes>
        {/* If you rename files/paths, update routes here */}
        //Public Routes
        <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />}></Route>

        //Protected Routes
        <Route path="/userInput" element={<ProtectedRoute><UserInput /></ProtectedRoute>} />
        <Route path="/takePicture" element={<ProtectedRoute><TakePicture /></ProtectedRoute>} />
        <Route path="/instructions" element={<ProtectedRoute><Instructions /></ProtectedRoute>} />
        <Route path="/output" element={<ProtectedRoute><Output /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}

function App() {
  return(
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App
