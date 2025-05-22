import RegisterForm from '../../components/Auth/RegisterForm'
import '../../styles/registerpage.css'

const Register = () => {
  return (
    <div className="register-page">
      <div className="register-container">
        <RegisterForm className="register-card-effect" />
      </div>
    </div>
  )
}

export default Register