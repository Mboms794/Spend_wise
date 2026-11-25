
import { useState } from 'react'
import {
  Wallet,
  LayoutDashboard,
  ChartNoAxesCombined,
  ArrowLeftRight,
  FileText,
  Settings,
  Search,
  Bell,
  Sun,
  Moon,
  ArrowUpRight,
  ArrowDownLeft,
  MoreVertical,
  ShoppingBag,
  Monitor,
  Utensils,
  Zap,
  Sparkles,
} from 'lucide-react'

import '../App.css'

const transactions = [
  { name: 'Grocery Shopping', category: 'Shopping', date: 'Today', amount: '-₦25,000', icon: ShoppingBag, type: 'expense' },
  { name: 'Salary Payment', category: 'Income', date: 'Yesterday', amount: '+₦250,000', icon: Wallet, type: 'income' },
  { name: 'Netflix Subscription', category: 'Entertainment', date: 'Nov 23', amount: '-₦8,500', icon: Monitor, type: 'expense' },
  { name: 'Restaurant', category: 'Food & Dining', date: 'Nov 22', amount: '-₦12,500', icon: Utensils, type: 'expense' },
  { name: 'Electricity Bill', category: 'Utilities', date: 'Nov 21', amount: '-₦15,000', icon: Zap, type: 'expense' },
]

const categories = [
  { name: 'Food & Dining', percent: 30, color: '#36e6b2' },
  { name: 'Shopping', percent: 24, color: '#16c76b' },
  { name: 'Utilities', percent: 20, color: '#00a8bd' },
  { name: 'Transport', percent: 16, color: '#ff7379' },
  { name: 'Subscriptions', percent: 10, color: '#075b49' },
]

const navigation = [
  { name: 'Dashboard', icon: LayoutDashboard },
  { name: 'Analytics', icon: ChartNoAxesCombined },
  { name: 'Transactions', icon: ArrowLeftRight },
  { name: 'Reports', icon: FileText },
  { name: 'Settings', icon: Settings },
]
const chartPeriods = {
  Week: {
    path: 'M0 120 C60 90 80 140 130 100 S190 65 250 110 S320 145 370 90 S450 75 500 95',
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  },

  Month: {
    path: 'M0 100 C35 95 35 145 75 130 S115 45 150 55 S205 110 240 95 S285 150 320 120 S365 75 400 95 S460 130 500 105',
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  },

  Year: {
    path: 'M0 140 C40 110 70 80 110 100 S170 130 210 70 S280 50 320 90 S390 120 430 65 S470 45 500 35',
    labels: ['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov'],
  },
}
function Dashboard() {
  const [theme, setTheme] = useState('dark')
  const [activePage, setActivePage] = useState('Dashboard')
  const [period, setPeriod] = useState('Month')
  const activeTrendPath = chartPeriods[period].path
  const activeLabels = chartPeriods[period].labels

  function toggleTheme() {
    const nextTheme = theme === 'dark' ? 'light' : 'dark'
    setTheme(nextTheme)
    document.documentElement.dataset.theme = nextTheme
  }

  return (
    <main className={`dashboard-page ${theme}`}>
      <div className="dashboard-shell">

        {/* HEADER */}
        <header className="topbar">
          <div className="brand">
            <div className="brand-icon">
              <ChartNoAxesCombined size={25} strokeWidth={2.5} />
            </div>
            <span className="brand-name">SpendWise</span>
          </div>

          <nav className="top-navigation">
            {navigation.map((item) => {
              const Icon = item.icon

              return (
                <button
                  key={item.name}
                  className={`top-nav-item ${
                    activePage === item.name ? 'selected' : ''
                  }`}
                  onClick={() => setActivePage(item.name)}
                >
                  <Icon size={15} />
                  {item.name}
                </button>
              )
            })}
          </nav>

          <div className="topbar-actions">
            <button className="round-button" aria-label="Search">
              <Search size={17} />
            </button>

            <button className="round-button" aria-label="Notifications">
              <Bell size={17} />
            </button>

            <button
              className="round-button"
              onClick={toggleTheme}
              aria-label="Change theme"
            >
              {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
            </button>

            <div className="profile-avatar">SW</div>
          </div>
        </header>

        {/* WELCOME */}
        <section className="welcome-row">
          <div>
            <h1><span>Welcome back,</span> there.</h1>
            <p>Here's your financial overview.</p>
          </div>

          <div className="period-switch">
            {['Week', 'Month', 'Year'].map((item) => (
              <button
                key={item}
                className={period === item ? 'period-active' : ''}
                onClick={() => setPeriod(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </section>

        {/* FINANCIAL OVERVIEW */}
        <section className="financial-overview">
          <div className="balance-section">
            <p className="eyebrow">TOTAL BALANCE</p>
            <h2>₦845,500<span>.00</span></h2>
            <p className="positive-change">
              ↗ 12.5% <span>compared to last month</span>
            </p>

            <div className="balance-actions">
              <button className="light-action">
                <ArrowUpRight size={16} /> Transfer
              </button>

              <button className="light-action">
                <ArrowDownLeft size={16} /> Receive
              </button>

              <button className="round-button" aria-label="More balance options">
                <MoreVertical size={17} />
              </button>
            </div>
          </div>

          <div className="overview-stat">
            <p className="eyebrow">TOTAL INCOME</p>
            <h3>₦450,000</h3>

            <div className="stat-bar income-bar">
              <span />
            </div>

            <p className="stat-caption">↗ 18.2% this month</p>
          </div>

          <div className="overview-stat">
            <p className="eyebrow">TOTAL EXPENSES</p>
            <h3>₦185,500</h3>

            <div className="mini-bars">
              {Array.from({ length: 22 }, (_, index) => (
                <span
                  key={index}
                  style={{ height: `${25 + ((index * 17) % 65)}%` }}
                />
              ))}
            </div>

            <p className="stat-caption">↘ Spending overview</p>
          </div>
        </section>

        {/* ANALYTICS */}
        <section className="analytics-grid">

          {/* INCOME AND EXPENSE CHART */}
          <div className="analytics-panel">
            <div className="panel-heading">
              <div>
                <h3>
                  <ChartNoAxesCombined size={17} /> Analytics
                </h3>
                <p>Income versus expenses</p>
              </div>

              <button className="round-button" aria-label="More analytics options">
                <MoreVertical size={17} />
              </button>
            </div>

            <div className="chart-legend">
              <span><i className="legend-income" /> Income</span>
              <span><i className="legend-expense" /> Expenses</span>
            </div>

            <div className="line-chart">
              <div className="chart-labels">
                <span>₦300k</span>
                <span>₦200k</span>
                <span>₦100k</span>
              </div>

              <svg
                viewBox="0 0 500 190"
                preserveAspectRatio="none"
                role="img"
                aria-label="Illustrative animated income and expense trend chart"
              >
                <defs>
                  <linearGradient
                    id="incomeGradient"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop
                      offset="0%"
                      stopColor="#16d69e"
                      stopOpacity=".24"
                    />
                    <stop
                      offset="100%"
                      stopColor="#16d69e"
                      stopOpacity="0"
                    />
                  </linearGradient>
                </defs>

                {/* Green area below the trend */}
                <path
                  d={`${activeTrendPath} L500 190 L0 190 Z`}
                  fill="url(#incomeGradient)"
                />

                {/* Main green trend */}
                <path
                 d={activeTrendPath}
                  fill="none"
                  stroke="#16d69e"
                  strokeWidth="3"
                />

                {/* Moving green highlight */}
                <path
                 d={activeTrendPath}
                  fill="none"
                  stroke="#d4fff0"
                  strokeWidth="3"
                  strokeDasharray="15 485"
                  className="moving-trend"
                />

                {/* Red expense trend */}
                <path
                  d="M0 145 C40 120 55 160 90 145 S130 165 165 130 S215 150 250 140 S300 165 340 140 S390 160 425 135 S470 155 500 145"
                  fill="none"
                  stroke="#ff7379"
                  strokeWidth="2"
                  strokeDasharray="5 5"
                  className="expense-trend"
                />

                {/* Moving indicator */}
                <circle
                  r="5"
                  fill="#36e6b2"
                  className="moving-dot"
                >
                  <animateMotion
                    dur="7s"
                    repeatCount="indefinite"
                    path={activeTrendPath}
                  />
                </circle>
              </svg>

              <div className="chart-months">
              {activeLabels.map((label) => (
              <span key={label}>{label}</span>
             ))}
              </div>
            </div>
          </div>

          {/* CATEGORY CHART */}
          <div className="analytics-panel">
            <div className="panel-heading">
              <div>
                <h3>
                  <Wallet size={17} /> Spending by category
                </h3>
                <p>Where your money goes</p>
              </div>

              <button className="round-button" aria-label="Open category details">
                <ArrowUpRight size={17} />
              </button>
            </div>

            <div className="donut-area">
              <div className="donut-chart">
                <div className="donut-center">
                  <span>Total spent</span>
                  <strong>₦185,500</strong>
                </div>
              </div>
            </div>

            <div className="category-legend">
              {categories.map((category) => (
                <div key={category.name}>
                  <span>
                    <i style={{ background: category.color }} />
                    {category.name}
                  </span>
                  <strong>{category.percent}%</strong>
                </div>
              ))}
            </div>
          </div>

          {/* RECENT TRANSACTIONS */}
          <div className="analytics-panel transactions-panel">
            <div className="panel-heading">
              <div>
                <h3>
                  <ArrowLeftRight size={17} /> Recent transactions
                </h3>
                <p>Your latest financial activity</p>
              </div>

              <button className="round-button" aria-label="Search transactions">
                <Search size={16} />
              </button>
            </div>

            <div className="recent-list">
              {transactions.map((transaction) => {
                const Icon = transaction.icon

                return (
                  <div
                    className="recent-transaction"
                    key={transaction.name}
                  >
                    <div className="recent-icon">
                      <Icon size={15} />
                    </div>

                    <div className="recent-description">
                      <strong>{transaction.name}</strong>
                      <span>{transaction.category}</span>
                    </div>

                    <strong
                      className={
                        transaction.type === 'income'
                          ? 'amount-income'
                          : 'amount-expense'
                      }
                    >
                      {transaction.amount}
                    </strong>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* AI INSIGHTS */}
        <section className="insight-panel">
          <div className="insight-icon">
            <Sparkles size={20} />
          </div>

          <div>
            <h3>SpendWise Intelligence</h3>
            <p>
              Your spending overview is ready. Review your category budgets
              and keep your monthly expenses on track.
            </p>
          </div>

          <button
            className="insight-link"
            onClick={() => setActivePage('Analytics')}
          >
            Explore insights <ArrowUpRight size={15} />
          </button>
        </section>

        <footer className="dashboard-footer">
          SpendWise · Your money, your control.
        </footer>

      </div>
    </main>
  )
}

export default Dashboard
