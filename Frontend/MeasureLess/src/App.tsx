import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import UserInput from './userInput';
import TakePicture from './takePicture.tsx';

function Home() {
    return <h1>Home Page</h1>;
}


function App() {
    return (
        <>
            <BrowserRouter>
                {/* Navigation */}
                <nav>
                    <Link to="/">Home</Link> |{" "}
                    <Link to="/userInput.tsx">UserInput</Link> |{" "}
                    <Link to="/takePicture.tsx">TakePicture</Link>
                </nav>

                {/* Routes */}
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/userInput.tsx" element={<UserInput />} />
                    <Route path="/takePicture.tsx" element={<TakePicture />} />
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default App
