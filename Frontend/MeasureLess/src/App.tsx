import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

function App() {
    const [count, setCount] = useState(0)

    return (
        <>
            <div className='max-w-7xl mx-auto px-8 text-center'>
                <div className='flex justify-center gap-12 py-12'>
                    <a href="https://vite.dev" target="_blank" className='group'>
                        <img
                            src={viteLogo}
                            className='h-24 p-6 transition-all duration-300 hover:drop-shadow-[0-0-2em_#646cffaa]'
                            alt="Vite logo"
                        />
                    </a>
                    <a href="https://react.dev" target="_blank" className="group">
                        <img
                            src={reactLogo}
                            className="h-24 p-6 transition-all duration-300 hover:drop-shadow-[0_0_2em_#61dafbaa] motion-safe:animate-[spin_20s_linear_infinite]"
                            alt="React logo"
                        />
                    </a>
                </div>
                <h1 className="text-5xl font-bold leading-tight mb-8">Vite + React</h1>
                <div className="p-8">
                    <button
                        onClick={() => setCount((count) => count + 1)}
                        className="rounded-lg border border-transparent px-5 py-2.5 text-base font-medium bg-gray-900 dark:bg-gray-100 dark:text-gray-900 text-white cursor-pointer transition-colors hover:border-blue-500 focus:outline"
                    >
                        count is {count}
                    </button>
                    <p className="mt-4">
                        Edit <code className="bg-gray-600 px-2 py-1 rounded">src/App.tsx</code> and save to test HMR
                    </p>
                </div>

                <p className="text-gray-500 mt-4">
                    Click on the Vite and React logos to learn more
                </p>
            </div>
        </>
    )
}

export default App
