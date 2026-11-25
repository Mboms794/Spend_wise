
import {
  Wallet,
  ChartNoAxesCombined,
  Target,
  BellRing,
  BrainCircuit,
  CalendarDays,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import Navbar from '../components/navbar'

function Features() {
  const features = [
    {
      icon: Wallet,
      title: 'Expense Tracking',
      description:
        'Record and organise your expenses so you can understand where your money goes.',
    },
    {
      icon: Target,
      title: 'Budget Management',
      description:
        'Create budgets, set spending limits and monitor your progress across different categories.',
    },
    {
      icon: ChartNoAxesCombined,
      title: 'Spending Analytics',
      description:
        'Explore spending summaries, trends and reports that help you make informed decisions.',
    },
    {
      icon: BrainCircuit,
      title: 'AI-Powered Insights',
      description:
        'Get helpful spending observations and budget insights based on your financial activity.',
    },
    {
      icon: BellRing,
      title: 'Budget Alerts',
      description:
        'Stay informed when your spending approaches or exceeds your budget limits.',
    },
    {
      icon: CalendarDays,
      title: 'Event Expense Management',
      description:
        'Organise event expenses and keep track of the costs associated with your plans.',
    },
  ]

  return (
    <main className="info-page">
      <Navbar />

      <section className="info-hero">
        <span className="section-label">SPENDWISE FEATURES</span>

        <h1>
          Everything you need to
          <span> manage money smarter.</span>
        </h1>

        <p>
          Discover tools designed to make expense tracking,
          budgeting and financial planning easier.
        </p>
      </section>

      <section className="info-content">
        {features.map((feature, index) => {
          const Icon = feature.icon

          return (
            <div className="info-card" key={index}>
              <Icon size={28} />
              <h2>{feature.title}</h2>
              <p>{feature.description}</p>
            </div>
          )
        })}
      </section>

      <section className="info-cta">
        <h2>Ready to manage your money better?</h2>
        <p>Start using SpendWise to bring more clarity to your finances.</p>

        <Link to="/signup" className="nav-get-started">
          Get Started
        </Link>
      </section>
    </main>
  )
}

export default Features
