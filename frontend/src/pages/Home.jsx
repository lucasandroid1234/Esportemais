import { Link } from 'react-router-dom'
import '../styles/home.css'

const Home = () => {
  return (
    <div className="home-container">
      <h1 className="home-title">Bem-vindo ao Esporte+</h1>
      <p className="home-subtitle">Sistema de agendamento de quadras esportivas</p>
      
      <div className="button-group">
        <Link
          to="/quadras"
          className="action-button primary-button"
        >
          Ver Quadras Disponíveis
        </Link>
        <Link
          to="/minhas-reservas"
          className="action-button primary-button"
        >
          Minhas Reservas
        </Link>
      </div>
      
      <div className="button-group">
        <Link
          to="/login"
          className="action-button secondary-button"
        >
          Fazer Login
        </Link>
        <Link
          to="/register"
          className="action-button secondary-button"
        >
          Criar Conta
        </Link>
      </div>
    </div>
  )
}

export default Home