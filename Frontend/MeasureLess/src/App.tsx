import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import UserInput from './userInput';

function Home() {
    return <h1>Home Page</h1>;
}

function About() {
    return <h1>About Page</h1>;
}

function Contact() {
    return <h1>Contact Page</h1>;
}

function App() {
    return (
        <>
            <BrowserRouter>
                {/* Navigation */}
                <nav>
                    <Link to="/">Home</Link> |{" "}
                    <Link to="/about">About</Link> |{" "}
                    <Link to="/contact">Contact</Link> |{" "}
                    <Link to="/userInput.tsx">UserInput</Link>
                </nav>

                {/* Routes */}
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/contact" element={<Contact />} />
                    <Route path="/userInput.tsx" element={<UserInput />} />
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default App
