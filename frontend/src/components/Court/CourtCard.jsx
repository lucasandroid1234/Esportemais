import { Link } from 'react-router-dom'

const CourtCard = ({ court }) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4">
        <h3 className="font-bold text-xl mb-2">{court.name}</h3>
        <p className="text-gray-600 mb-3">{court.location}</p>
        <p className="mb-3">{court.description}</p>
        
        <div className="flex flex-wrap gap-1 mb-4">
          {court.sports.map(sport => (
            <span key={sport} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
              {sport}
            </span>
          ))}
        </div>
        
        <Link
          to={`/agendar/${court.id}`}
          className="block w-full bg-green-600 text-white text-center py-2 px-4 rounded hover:bg-green-700"
        >
          Agendar
        </Link>
      </div>
    </div>
  )
}

export default CourtCard