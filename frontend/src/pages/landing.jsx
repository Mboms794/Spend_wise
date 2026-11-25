import Navbar from '../components/navbar'
import { Link } from 'react-router-dom'
import {
  ArrowRight,
  ShieldCheck,
  ChartNoAxesCombined,
  Wallet,
  Sparkles,
  CheckCircle2,
} from 'lucide-react'
import '../App.css'

function LandingPage({ theme, onToggleTheme }) {
  return (
    <main className="landing-page">
        <Navbar theme={theme} onToggleTheme={onToggleTheme} />
      <section className="landing-hero">
        <div className="landing-content">
          <div className="landing-badge">
            <Sparkles size={15} />
            Smarter money management starts here
          </div>

          <h1>
            Take control of
            <span> your money.</span>
          </h1>

          <p className="landing-description">
            Track your spending, manage your budgets and
            understand your financial habits — all in one
            simple and intelligent platform.
          </p>

          <div className="landing-actions">
            <Link to="/signup" className="primary-cta">
              Get Started
              <ArrowRight size={18} />
            </Link>

            <Link to="/signin" className="secondary-cta">
              Sign In
            </Link>
          </div>

          <div className="landing-trust">
            <span><ShieldCheck size={16} /> Secure accounts</span>
            <span><CheckCircle2 size={16} /> Simple tracking</span>
          </div>
        </div>

        <div className="landing-preview">
          <div className="preview-card">
            <div className="preview-heading">
              <div>
                <span className="preview-label">Total balance</span>
                <h2>₦2,450,000</h2>
              </div>
              <div className="preview-icon">
                <Wallet size={23} />
              </div>
            </div>

            <div className="preview-divider" />

            <div className="preview-stats">
              <div>
                <span>Income</span>
                <strong>₦850,000</strong>
              </div>
              <div>
                <span>Expenses</span>
                <strong>₦320,000</strong>
              </div>
            </div>

            <div className="preview-chart">
              <div className="preview-chart-heading">
                <span>Spending overview</span>
                <ChartNoAxesCombined size={18} />
              </div>

              <svg viewBox="0 0 400 130" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="landingGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity=".35" />
                    <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
                  </linearGradient>
                </defs>

                <path
                  d="M0 105 C45 95 55 45 105 65 S165 110 205 70 S270 30 310 55 S365 25 400 10 L400 130 L0 130 Z"
                  fill="url(#landingGradient)"
                />

                <path
                  d="M0 105 C45 95 55 45 105 65 S165 110 205 70 S270 30 310 55 S365 25 400 10"
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </svg>
            </div>

            <div className="preview-footer">
              <span><span className="status-dot" /> Your finances at a glance</span>
              <Sparkles size={16} />
            </div>
          </div>
        </div>
      </section>

      <section className="landing-features">
        <div className="features-heading">
          <span>WHY SPENDWISE?</span>
          <h2>Everything you need to manage money better.</h2>
          <p>One platform. Clear insights. Better financial decisions.</p>
        </div>

        <div className="feature-grid">
          <article className="feature-card">
            <Wallet size={25} />
            <h3>Track expenses</h3>
            <p>Keep track of your income and expenses in one organised place.</p>
          </article>

          <article className="feature-card">
            <ChartNoAxesCombined size={25} />
            <h3>Understand your spending</h3>
            <p>Explore your spending patterns through clear financial analytics.</p>
          </article>

          <article className="feature-card">
            <Sparkles size={25} />
            <h3>Smart insights</h3>
            <p>Get helpful insights that make it easier to understand your budget.</p>
          </article>
        </div>
      </section>
    </main>
  )
}

export default LandingPage
