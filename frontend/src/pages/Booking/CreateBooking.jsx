import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import api from '../../api/api'
import BookingForm from '../../components/Booking/BookingForm'
import { format, addDays, isToday, isBefore } from 'date-fns'
import { ptBR } from 'date-fns/locale'

const CreateBooking = () => {
  const { courtId } = useParams()
  const navigate = useNavigate()
  const [court, setCourt] = useState(null)
  const [availableSlots, setAvailableSlots] = useState([])
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  const formatBrazilianDate = (date) => {
    return format(date, "EEEE, d 'de' MMMM", { locale: ptBR })
  }

  useEffect(() => {
    const fetchCourtData = async () => {
      setLoading(true)
      try {
        const [courtResponse, slotsResponse] = await Promise.all([
          api.get(`/courts/${courtId}`),
          api.get(`/courts/${courtId}/availability`, {
            params: { date: format(selectedDate, 'yyyy-MM-dd') }
          })
        ])
        
        setCourt(courtResponse.data)
        setAvailableSlots(slotsResponse.data)
      } catch (error) {
        toast.error('Erro ao carregar dados da quadra')
        console.error('Erro:', error)
        navigate('/quadras')
      } finally {
        setLoading(false)
      }
    }
    
    fetchCourtData()
  }, [courtId, selectedDate, navigate])

  const handleDateChange = (days) => {
    const newDate = addDays(selectedDate, days)
    
    if (isBefore(newDate, new Date()) && !isToday(newDate)) {
      toast.warning('Não é possível agendar para datas passadas')
      return
    }
    
    setSelectedDate(newDate)
  }

  const handleBookingSubmit = async (bookingData) => {
    if (!bookingData.time) {
      toast.warning('Selecione um horário para agendar')
      return
    }

    setSubmitting(true)
    
    try {
      await api.post('/bookings', {
        courtId,
        date: format(selectedDate, 'yyyy-MM-dd'),
        ...bookingData
      })
      
      toast.success('Reserva realizada com sucesso!')
      navigate('/minhas-reservas')
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Erro ao realizar reserva'
      toast.error(errorMessage)
      console.error('Erro ao criar reserva:', error)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (!court) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold">Quadra não encontrada</h2>
        <button 
          onClick={() => navigate('/quadras')} 
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Voltar para lista de quadras
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">
        Agendar Quadra: <span className="text-blue-600">{court.name}</span>
      </h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <button 
            onClick={() => handleDateChange(-1)} 
            disabled={isToday(selectedDate)}
            className={`px-4 py-2 rounded ${
              isToday(selectedDate) 
                ? 'bg-gray-200 cursor-not-allowed' 
                : 'bg-blue-100 hover:bg-blue-200'
            }`}
          >
            Dia Anterior
          </button>
          
          <span className="font-medium text-lg">
            {formatBrazilianDate(selectedDate)}
          </span>
          
          <button 
            onClick={() => handleDateChange(1)} 
            className="px-4 py-2 bg-blue-100 rounded hover:bg-blue-200"
          >
            Próximo Dia
          </button>
        </div>
        
        <div className="border-t pt-4">
          <p className="text-gray-600 mb-2">
            <span className="font-semibold">Local:</span> {court.location}
          </p>
          <p className="text-gray-600">
            <span className="font-semibold">Esportes:</span> {court.sports.join(', ')}
          </p>
        </div>
      </div>
      
      <BookingForm 
        availableSlots={availableSlots} 
        onSubmit={handleBookingSubmit}
        submitting={submitting}
      />
    </div>
  )
}

export default CreateBooking