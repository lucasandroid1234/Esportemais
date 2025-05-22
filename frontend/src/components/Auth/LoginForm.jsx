// Front-end/src/components/Auth/LoginForm.jsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../../api/api'
import '../../styles/login.css'

const LoginForm = () => {
  const [formData, setFormData] = useState({
    cpf: '',
    password: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      // Formato esperado pelo OAuth2PasswordRequestForm
      const response = await authAPI.login(formData.cpf, formData.password)
      
      if (response.data.access_token) {
        localStorage.setItem('authToken', response.data.access_token)
        navigate('/quadras')
      }
    } catch (err) {
      setError('CPF ou senha incorretos')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <h2 className="login-title">Login</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="form-group">
        <label className="form-label">CPF</label>
        <input
          type="text"
          name="cpf"
          value={formData.cpf}
          onChange={handleChange}
          required
          className="form-input"
          placeholder="Digite seu CPF"
        />
      </div>
      
      <div className="form-group">
        <label className="form-label">Senha</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className="form-input"
          placeholder="Digite sua senha"
        />
      </div>
      
      <button
        type="submit"
        disabled={loading}
        className="submit-button"
      >
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  )
}

export default LoginForm