const BookingCard = ({ booking, onCancel }) => {
  const formatDate = (dateString) => {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric' }
    return new Date(dateString).toLocaleDateString('pt-BR', options)
  }

  return (
    <div className="bg-white p-4 rounded shadow">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-bold text-lg">{booking.court.name}</h3>
          <p className="text-gray-600">{booking.court.location}</p>
          <p className="mt-2">
            <span className="font-medium">Data:</span> {formatDate(booking.date)}
          </p>
          <p>
            <span className="font-medium">Horário:</span> {booking.time}
          </p>
          <p>
            <span className="font-medium">Esporte:</span> {booking.sport}
          </p>
          <p className={`mt-2 px-2 py-1 inline-block rounded ${
            booking.status === 'confirmed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
          }`}>
            {booking.status === 'confirmed' ? 'Confirmado' : 'Pendente'}
          </p>
        </div>
        
        <button
          onClick={() => onCancel(booking.id)}
          className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
        >
          Cancelar
        </button>
      </div>
    </div>
  )
}

export default BookingCard