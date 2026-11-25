
import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

import LandingPage from './pages/landing'
import Dashboard from './components/dashboard'
import Signin from './pages/Signin'
import Signup from './pages/Signup'
import About from './pages/About'
import Features from './pages/Features'
import HowItWorks from './pages/Howitworks'

function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('spendwise-theme') || 'dark'
  })

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('spendwise-theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(current => current === 'dark' ? 'light' : 'dark')
  }

  return (
    <BrowserRouter>
      
<Routes>
  <Route
    path="/"
    element={
      <LandingPage
        theme={theme}
        onToggleTheme={toggleTheme}
      />
    }
  />
  <Route path="/about" element={<About />} />
  <Route path="/features" element={<Features />} />
  <Route path="/how-it-works" element={<HowItWorks />} />
  <Route path="/signin" element={<Signin />} />
  <Route path="/signup" element={<Signup />} />
  <Route path="/dashboard" element={<Dashboard />} />
  <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
    </BrowserRouter>
  )
}

export default App

