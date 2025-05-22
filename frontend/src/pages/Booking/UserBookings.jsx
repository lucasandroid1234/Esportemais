import { useState, useEffect } from 'react'
import api from '../../api/api'
import BookingCard from '../../components/Booking/BookingCard'

const UserBookings = () => {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await api.get('/bookings/user')
        setBookings(response.data)
      } finally {
        setLoading(false)
      }
    }
    
    fetchBookings()
  }, [])

  const handleCancel = async (bookingId) => {
    try {
      await api.delete(`/bookings/${bookingId}`)
      setBookings(bookings.filter(b => b.id !== bookingId))
    } catch (error) {
      console.error('Erro ao cancelar reserva:', error)
    }
  }

  if (loading) return <div>Carregando suas reservas...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Minhas Reservas</h1>
    </div>
  )
}

export default UserBookings