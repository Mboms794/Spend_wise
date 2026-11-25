
import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Wallet,
  Eye,
  EyeOff,
  ArrowRight,
  CheckCircle2,
} from 'lucide-react'
import '../App.css'

function Signin() {
  const [showPassword, setShowPassword] = useState(false)

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    })
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    alert('Sign in interface is ready. Backend connection comes next.')
  }

  return (
    <main className="auth-page">
      <div className="auth-decoration auth-decoration-one" />
      <div className="auth-decoration auth-decoration-two" />

      <Link to="/" className="auth-brand">
        <span className="auth-brand-icon">
          <Wallet size={22} />
        </span>
        Spend<span>Wise</span>
      </Link>

      <section className="auth-container">
        <div className="auth-heading">
          <span className="section-label">WELCOME BACK</span>
          <h1>Sign in to SpendWise</h1>
          <p>
            Welcome back! Let's get you back to managing your finances.
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-input-group">
            <label htmlFor="username">Username or email</label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="Enter your username or email"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="auth-input-group">
            <label htmlFor="password">Password</label>

            <div className="auth-password-wrapper">
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
                required
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={
                  showPassword ? 'Hide password' : 'Show password'
                }
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <div className="auth-benefit">
            <CheckCircle2 size={17} />
            <span>Your finances, organised in one place.</span>
          </div>

          <button type="submit" className="auth-submit">
            Sign In <ArrowRight size={18} />
          </button>
        </form>

        <p className="auth-switch">
          Don't have an account? <Link to="/signup">Create account</Link>
        </p>

        <Link to="/" className="auth-back-home">
          Back to homepage
        </Link>
      </section>

      <p className="auth-footer">
        © 2026 SpendWise. Manage your money with confidence.
      </p>
    </main>
  )
}

export default Signin
