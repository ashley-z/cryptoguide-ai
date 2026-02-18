import { useState, useCallback } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'
import ProtocolSelector from './components/ProtocolSelector'
import SuggestedQuestions from './components/SuggestedQuestions'

const PROTOCOLS = [
  { id: 'aave', name: 'Aave', icon: '🏦' },
  { id: 'compound', name: 'Compound', icon: '🔬' },
  { id: 'uniswap', name: 'Uniswap', icon: '🦄' },
]

function App() {
  const [selectedProtocol, setSelectedProtocol] = useState('aave')
  const [compareProtocol, setCompareProtocol] = useState('compound')
  const [compareMode, setCompareMode] = useState(false)
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [inputValue, setInputValue] = useState('')

  const handleSubmit = useCallback(async (question) => {
    if (!question.trim() || isLoading) return

    const userMessage = { role: 'user', content: question }
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      let url, body

      if (compareMode) {
        url = '/api/compare'
        body = {
          question,
          protocols: [selectedProtocol, compareProtocol],
        }
      } else {
        url = '/api/query'
        body = {
          question,
          protocol: selectedProtocol,
        }
      }

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })

      if (!response.ok) throw new Error(`API error: ${response.status}`)

      const data = await response.json()
      const assistantMessage = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources || [],
        metadata: data.metadata || {},
        isComparison: compareMode,
        protocols: compareMode ? data.protocols : undefined,
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Query failed:', error)
      const errorMessage = {
        role: 'assistant',
        content: "I couldn't process that question. Please ensure the backend server is running on port 8000.",
        isError: true,
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }, [isLoading, selectedProtocol, compareProtocol, compareMode])

  const handleSuggestedQuestion = useCallback((question) => {
    setInputValue(question)
  }, [])

  const protocolName = PROTOCOLS.find(p => p.id === selectedProtocol)?.name || 'Protocol'
  const compareProtocolName = PROTOCOLS.find(p => p.id === compareProtocol)?.name || 'Protocol'

  const availableCompareProtocols = PROTOCOLS.filter(p => p.id !== selectedProtocol)

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header glass">
        <div className="header-left">
          <div className="logo">
            <span className="logo-icon">◇</span>
            <h1 className="logo-text">CryptoGuide<span className="logo-accent">AI</span></h1>
          </div>
          <span className="header-tag">DeFi Research Assistant</span>
        </div>
        <div className="header-right">
          <ProtocolSelector
            protocols={PROTOCOLS}
            selected={selectedProtocol}
            onChange={setSelectedProtocol}
            compareMode={compareMode}
            compareProtocol={compareProtocol}
            onCompareProtocolChange={setCompareProtocol}
            onToggleCompare={() => setCompareMode(!compareMode)}
            availableCompareProtocols={availableCompareProtocols}
          />
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {messages.length === 0 ? (
          <div className="welcome-screen animate-fade-in">
            <div className="welcome-hero">
              <div className="welcome-prism">◇</div>
              <h2 className="welcome-title">
                {compareMode ? (
                  <>Compare <span className="text-gradient">{protocolName}</span> vs <span className="text-gradient">{compareProtocolName}</span></>
                ) : (
                  <>Ask anything about <span className="text-gradient">{protocolName}</span></>
                )}
              </h2>
              <p className="welcome-subtitle">
                {compareMode
                  ? 'Get side-by-side analysis with citations from both protocol docs.'
                  : 'Get accurate, cited answers from protocol documentation in seconds.'}
              </p>
            </div>
            <SuggestedQuestions
              protocol={compareMode ? 'compare' : selectedProtocol}
              onSelect={handleSuggestedQuestion}
            />
          </div>
        ) : (
          <ChatInterface
            messages={messages}
            isLoading={isLoading}
          />
        )}
      </main>

      {/* Input Bar */}
      <footer className="app-footer">
        <form
          className="input-container"
          onSubmit={(e) => {
            e.preventDefault()
            handleSubmit(inputValue)
          }}
        >
          <div className="input-wrapper">
            <input
              type="text"
              className="query-input"
              placeholder={compareMode
                ? `Compare ${protocolName} vs ${compareProtocolName}...`
                : `Ask about ${protocolName}...`}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isLoading}
              autoFocus
            />
            <button
              type="submit"
              className="submit-btn"
              disabled={isLoading || !inputValue.trim()}
            >
              {isLoading ? (
                <span className="submit-loading">⟳</span>
              ) : (
                <span>→</span>
              )}
            </button>
          </div>
          <p className="input-disclaimer">
            Answers are generated from protocol documentation. Always verify before making financial decisions.
          </p>
        </form>
      </footer>
    </div>
  )
}

export default App
