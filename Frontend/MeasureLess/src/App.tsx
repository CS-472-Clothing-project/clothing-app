import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import UserInput from './userInput'
import TakePicture from './takePicture.tsx'
import Instructions from './instructions' 
import Output from './output.tsx'

function Home() {
  return <h1>Home Page</h1>
}


function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link> |{" "}
        <Link to="/userInput.tsx">UserInput</Link> |{" "}
        <Link to="/takePicture.tsx">TakePicture</Link> |{" "}
        <Link to="/instructions">Instructions</Link>  |{" "}
        <Link to="/output">Output</Link> |{" "}
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/userInput.tsx" element={<UserInput />} />
        <Route path="/takePicture.tsx" element={<TakePicture />} />
        <Route path="/instructions" element={<Instructions />} /> {" "}
        <Route path="/output" element={<Output />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
