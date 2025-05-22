// Front-end/src/api/api.js
import axios from 'axios'
import { toast } from 'react-toastify'
import { useNavigate } from 'react-router-dom'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000', // Adicione um fallback
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true // Para lidar com cookies se necessário
})

// Interceptor para adicionar token JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => {
    // Tratar respostas bem-sucedidas
    if (response.data?.access_token) {
      localStorage.setItem('authToken', response.data.access_token)
    }
    return response
  },
  (error) => {
    // Tratar erros
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      window.location.href = '/login'
      toast.error('Sessão expirada. Faça login novamente.')
    }
    
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        'Erro na requisição'
    
    if (errorMessage && error.response?.status !== 401) {
      toast.error(errorMessage)
    }
    
    return Promise.reject(error)
  }
)

// Funções específicas da API
export const authAPI = {
  login: (cpf, senha) => api.post('/usuario/login', { username: cpf, password: senha }),
  register: (userData) => api.post('/usuario/cadastrar', userData),
  resetPassword: (email, cpf) => api.post('/usuario/redefinir-senha', { email, cpf })
}

export const quadrasAPI = {
  listar: () => api.get('/quadras/listar-quadras'),
  detalhes: (id) => api.get(`/quadras/listar-quadras/${id}`),
  horariosDisponiveis: (id, data) => api.get('/quadras/horarios-disponiveis', { 
    params: { id_quadra: id, data } 
  })
}

export const agendamentosAPI = {
  criar: (agendamento) => api.post('/agendamentos/agendar-quadra', agendamento),
  listar: () => api.get('/agendamentos/'),
  cancelar: (id) => api.put(`/agendamentos/cancelar/${id}`)
}

export default api