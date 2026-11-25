import {
  Wallet,
  Sun,
  Moon,
  Menu,
  X,
  ArrowRight,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { useState } from 'react'

function Navbar({ theme, onToggleTheme }) {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="site-navbar">
      <Link to="/" className="site-brand">
        <span className="brand-icon">
          <Wallet size={21} />
        </span>
        <span>Spend<span>Wise</span></span>
      </Link>

      <nav className={`site-nav ${menuOpen ? 'nav-open' : ''}`}>
            <Link to="/" onClick={() => setMenuOpen(false)}>
        Home
        </Link>
            <Link to="/about" onClick={() => setMenuOpen(false)}>
        About Us
        </Link>
            <Link to="/features" onClick={() => setMenuOpen(false)}>
        Features
        </Link>
            <Link to="/how-it-works" onClick={() => setMenuOpen(false)}>
        How It Works
        </Link>
        
        <div className="mobile-nav-actions">
          <Link to="/signin" className="nav-signin">Sign In</Link>
          <Link to="/signup" className="nav-get-started">
            Get Started <ArrowRight size={16} />
          </Link>
        </div>
      </nav>

      <div className="nav-actions">
        <button
          className="theme-toggle"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          title="Change theme"
        >
          {theme === 'dark' ? <Sun size={19} /> : <Moon size={19} />}
        </button>

        <Link to="/signin" className="nav-signin desktop-action">
          Sign In
        </Link>

        <Link to="/signup" className="nav-get-started desktop-action">
          Get Started <ArrowRight size={16} />
        </Link>

        <button
          className="mobile-menu-button"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle navigation menu"
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>
    </header>
  )
}

export default Navbar
