
import { Target, Eye, Heart, Users } from 'lucide-react'
import { Link } from 'react-router-dom'
import Navbar from '../components/navbar'

function About() {
  return (
    <main className="info-page">
      <Navbar />

      <section className="info-hero">
        <span className="section-label">ABOUT SPENDWISE</span>

        <h1>
          Making financial management
          <span> simpler and smarter.</span>
        </h1>

        <p>
          SpendWise helps individuals, businesses, organisations and
          event planners understand their spending, manage budgets
          and make better financial decisions.
        </p>
      </section>

      <section className="info-content">
        <div className="info-card">
          <Target size={28} />
          <h2>Our Mission</h2>
          <p>
            To empower individuals, businesses, organisations and
            event planners to take control of their finances through
            intelligent expense tracking, effective budgeting and
            actionable financial insights.
          </p>
        </div>

        <div className="info-card">
          <Eye size={28} />
          <h2>Our Vision</h2>
          <p>
            To make smarter financial management accessible to
            everyone through simple, useful and intelligent
            financial technology.
          </p>
        </div>

        <div className="info-card">
          <Heart size={28} />
          <h2>What We Believe</h2>
          <p>
            Everyone deserves clarity and control over their money.
            Good financial decisions begin with understanding
            where money goes.
          </p>
        </div>

        <div className="info-card">
          <Users size={28} />
          <h2>Who We Serve</h2>
          <p>
            Our platform is designed for individuals, growing
            businesses, organisations and event planners who
            want a clearer picture of their finances.
          </p>
        </div>
      </section>

      <section className="info-cta">
        <h2>Take control of your finances.</h2>
        <p>Start making more informed financial decisions with SpendWise.</p>
        <Link to="/signup" className="nav-get-started">
          Get Started
        </Link>
      </section>
    </main>
  )
}

export default About
