import { useEffect, useState } from 'react'
import { toast } from 'react-toastify'
import api from '../../api/api'
import CourtCard from '../../components/Court/CourtCard'

const CourtList = () => {
  const [courts, setCourts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchCourts = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const response = await api.get('/courts')
      
        if (response.data && Array.isArray(response.data)) {
          setCourts(response.data)
        } else {
          throw new Error('Formato de dados inválido da API')
        }
      } catch (err) {
        console.error('Erro ao buscar quadras:', err)
        setError('Não foi possível carregar as quadras disponíveis')
        toast.error('Erro ao carregar quadras')
      } finally {
        setLoading(false)
      }
    }
    
    fetchCourts()
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[300px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
        <p className="text-gray-600">Carregando quadras disponíveis...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold text-red-600 mb-4">{error}</h2>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Tentar novamente
        </button>
      </div>
    )
  }

  if (courts.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold mb-4">Nenhuma quadra disponível no momento</h2>
        <p className="text-gray-600 mb-4">Por favor, tente novamente mais tarde.</p>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Recarregar
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Quadras Disponíveis</h1>
        <div className="text-sm text-gray-500">
          {courts.length} {courts.length === 1 ? 'quadra' : 'quadras'} encontradas
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {courts.map(court => (
          <CourtCard key={court.id} court={court} />
        ))}
      </div>
    </div>
  )
}

export default CourtList