// Front-end/src/components/Layout/Header.jsx
import { Link, useNavigate } from 'react-router-dom'
import api from '../../api/api'
import '../../styles/header.css'

const Header = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    navigate('/login')
  }

  return (
    <header className="app-header">
      <div className="header-container">
        <Link to="/" className="app-logo">Esporte+</Link>
        
        <nav className="nav-menu">
          <Link to="/quadras" className="nav-item">Quadras</Link>
          <Link to="/minhas-reservas" className="nav-item">Minhas Reservas</Link>
          <button onClick={handleLogout} className="logout-btn">Sair</button>
        </nav>
      </div>
    </header>
  )
}

export default Header