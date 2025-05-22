import LoginForm from '../../components/Auth/LoginForm'
import "../../styles/login.css";

const Login = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4">
      <LoginForm />
    </div>
  )
}

export default Login