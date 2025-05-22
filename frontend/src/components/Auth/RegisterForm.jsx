import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../../api/api'
import '../../styles/registerform.css'

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    
    // Limpa mensagens de erro quando o usuário digita
    if (error) setError('')
  }

  const validateForm = () => {
    if (!formData.nome || !formData.cpf || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('Todos os campos são obrigatórios')
      return false
    }

    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem')
      return false
    }

    if (formData.password.length < 8) {
      setError('A senha deve ter no mínimo 8 caracteres')
      return false
    }

    // Validação simples de CPF (apenas tamanho)
    if (formData.cpf.length !== 11 || !/^\d+$/.test(formData.cpf)) {
      setError('CPF deve conter 11 dígitos numéricos')
      return false
    }

    // Validação simples de email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      setError('Por favor, insira um email válido')
      return false
    }

    return true
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const response = await authAPI.register({
        nome: formData.nome.trim(),
        cpf: formData.cpf.replace(/\D/g, ''), // Remove não-dígitos
        email: formData.email.trim().toLowerCase(),
        senha: formData.password
      })
      
      if (response.status === 201) {
        setSuccess('Cadastro realizado com sucesso! Redirecionando...')
        setTimeout(() => navigate('/login'), 2000)
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 
                      err.response?.data?.message || 
                      'Erro ao cadastrar usuário. Tente novamente.'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="register-form">
      <h2 className="register-title">Criar Nova Conta</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {success && (
        <div className="success-message">
          {success}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="nome" className="form-label">Nome Completo</label>
        <input
          type="text"
          id="nome"
          name="nome"
          value={formData.nome}
          onChange={handleChange}
          className="form-input"
          placeholder="Digite seu nome completo"
          disabled={loading}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="cpf" className="form-label">CPF</label>
        <input
          type="text"
          id="cpf"
          name="cpf"
          value={formData.cpf}
          onChange={handleChange}
          className="form-input"
          placeholder="000.000.000-00"
          disabled={loading}
          maxLength={11}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="email" className="form-label">Email</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="form-input"
          placeholder="seu@email.com"
          disabled={loading}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="password" className="form-label">Senha</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          className="form-input"
          placeholder="Crie uma senha segura"
          disabled={loading}
          minLength={8}
        />
        <small className="form-hint">Mínimo 8 caracteres</small>
      </div>
      
      <div className="form-group">
        <label htmlFor="confirmPassword" className="form-label">Confirmar Senha</label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          className={`form-input ${
            formData.password && formData.confirmPassword && 
            formData.password !== formData.confirmPassword ? 'input-error' : ''
          }`}
          placeholder="Repita sua senha"
          disabled={loading}
        />
      </div>
      
      <button
        type="submit"
        disabled={loading}
        className={`submit-button ${loading ? 'loading' : ''}`}
      >
        {loading ? (
          <>
            <span className="spinner"></span>
            Processando...
          </>
        ) : 'Registrar'}
      </button>
      
      <p className="login-link-text">
        Já tem uma conta? <a href="/login" className="login-link">Faça login</a>
      </p>
    </form>
  )
}

export default RegisterForm