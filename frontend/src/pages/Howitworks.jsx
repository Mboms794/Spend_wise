
import {
  UserPlus,
  Wallet,
  Target,
  ChartNoAxesCombined,
  BrainCircuit,
  ArrowRight,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import Navbar from '../components/navbar'

function HowItWorks() {
  const steps = [
    {
      number: '01',
      icon: UserPlus,
      title: 'Create Your Account',
      description:
        'Sign up for SpendWise and create your personal account to get started.',
    },
    {
      number: '02',
      icon: Wallet,
      title: 'Record Your Expenses',
      description:
        'Add your income and expenses, organise transactions and keep your financial records in one place.',
    },
    {
      number: '03',
      icon: Target,
      title: 'Set Your Budgets',
      description:
        'Create spending limits and organise your budgets around the categories that matter to you.',
    },
    {
      number: '04',
      icon: ChartNoAxesCombined,
      title: 'Monitor Your Spending',
      description:
        'Review your dashboard, reports and spending trends to understand your financial activity.',
    },
    {
      number: '05',
      icon: BrainCircuit,
      title: 'Get Financial Insights',
      description:
        'Use helpful spending insights to identify patterns and make more informed financial decisions.',
    },
  ]

  return (
    <main className="info-page">
      <Navbar />

      <section className="info-hero">
        <span className="section-label">HOW IT WORKS</span>

        <h1>
          Managing your finances
          <span> made simple.</span>
        </h1>

        <p>
          Getting started with SpendWise is straightforward.
          Follow these steps to bring more structure and clarity
          to your financial management.
        </p>
      </section>

      <section className="steps-container">
        {steps.map((step, index) => {
          const Icon = step.icon

          return (
            <div className="step-card" key={step.number}>
              <div className="step-number">{step.number}</div>

              <div className="step-icon">
                <Icon size={27} />
              </div>

              <div className="step-details">
                <h2>{step.title}</h2>
                <p>{step.description}</p>
              </div>

              {index !== steps.length - 1 && (
                <div className="step-arrow">
                  <ArrowRight size={20} />
                </div>
              )}
            </div>
          )
        })}
      </section>

      <section className="info-cta">
        <h2>Your financial journey starts here.</h2>
        <p>Take the first step towards better financial management.</p>

        <Link to="/signup" className="nav-get-started">
          Create Your Account
        </Link>
      </section>
    </main>
  )
}

export default HowItWorks
