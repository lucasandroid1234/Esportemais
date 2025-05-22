import api from './api'

export const getCourts = async () => {
  try {
    const response = await api.get('/courts')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erro ao obter quadras')
  }
}

export const getAvailableSlots = async (courtId, date) => {
  try {
    const formattedDate = date.toISOString().split('T')[0]
    const response = await api.get(`/courts/${courtId}/availability`, {
      params: { date: formattedDate }
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erro ao obter horários disponíveis')
  }
}

export const createBooking = async (bookingData) => {
  try {
    const response = await api.post('/bookings', bookingData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erro ao criar agendamento')
  }
}

export const getUserBookings = async () => {
  try {
    const response = await api.get('/bookings/user')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erro ao obter agendamentos')
  }
}

export const cancelBooking = async (bookingId) => {
  try {
    const response = await api.delete(`/bookings/${bookingId}`)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erro ao cancelar agendamento')
  }
}