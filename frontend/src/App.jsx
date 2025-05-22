import { BrowserRouter } from 'react-router-dom'
import AppRoutes from './routes'
import Header from './components/Layout/Header'
import './styles/global.css'

function App() {
  return (
    <BrowserRouter>
        <div className="min-h-screen bg-gray-100">
          <Header />
          <main className="container mx-auto px-4 py-8">
            <AppRoutes />
          </main>
        </div>
    </BrowserRouter>
  )
}

export default App