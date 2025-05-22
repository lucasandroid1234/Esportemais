const BookingForm = ({ availableSlots, onSubmit }) => {
  const [selectedSlot, setSelectedSlot] = useState('')
  const [sport, setSport] = useState('futebol')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!selectedSlot) {
      alert('Selecione um horário')
      return
    }
    onSubmit({ time: selectedSlot, sport })
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow">
      <div className="mb-6">
        <h3 className="font-medium mb-3">Horários Disponíveis</h3>
        <div className="grid grid-cols-3 gap-2">
          {availableSlots.map(slot => (
            <button
              key={slot.time}
              type="button"
              onClick={() => setSelectedSlot(slot.time)}
              className={`p-2 border rounded ${
                selectedSlot === slot.time 
                  ? 'bg-blue-100 border-blue-500' 
                  : 'hover:bg-gray-100'
              } ${!slot.available && 'opacity-50 cursor-not-allowed'}`}
              disabled={!slot.available}
            >
              {slot.time}
            </button>
          ))}
        </div>
      </div>
      
      <div className="mb-6">
        <label className="block mb-2">Esporte</label>
        <select
          value={sport}
          onChange={(e) => setSport(e.target.value)}
          className="w-full p-2 border rounded"
        >
          <option value="futebol">Futebol</option>
          <option value="volei">Vôlei</option>
          <option value="basquete">Basquete</option>
          <option value="outro">Outro</option>
        </select>
      </div>
      
      <button
        type="submit"
        className="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
      >
        Confirmar Reserva
      </button>
    </form>
  )
}

export default BookingForm