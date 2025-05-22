import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Auth/Login'
import Register from './pages/Auth/Register'
import CourtList from './pages/Court/CourtList'
import CreateBooking from './pages/Booking/CreateBooking'
import UserBookings from './pages/Booking/UserBookings'

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/quadras" element={<CourtList />} />
      <Route path="/agendar/:courtId" element={<CreateBooking />} />
      <Route path="/minhas-reservas" element={<UserBookings />} />
    </Routes>
  )
}

export default AppRoutes