import './SuggestedQuestions.css'

const SUGGESTIONS = {
    aave: [
        { text: 'What are the risks of supplying USDC to Aave V3?', category: 'Risk' },
        { text: "What is Aave's liquidation threshold for ETH?", category: 'Parameters' },
        { text: 'How does flash loan protection work in Aave?', category: 'Mechanism' },
    ],
    compound: [
        { text: 'How does Compound V3 handle interest rates?', category: 'Basics' },
        { text: "How does Compound's governance work?", category: 'Governance' },
        { text: 'What are the borrowing limits on Compound V3?', category: 'Parameters' },
    ],
    uniswap: [
        { text: 'How does concentrated liquidity work in Uniswap V3?', category: 'Mechanism' },
        { text: 'What is impermanent loss on Uniswap?', category: 'Risk' },
        { text: 'How are swap fees calculated in Uniswap?', category: 'Parameters' },
    ],
    compare: [
        { text: 'Compare how liquidation works in Aave vs Compound', category: 'Compare' },
        { text: 'What are the differences in interest rate models?', category: 'Compare' },
        { text: 'Compare governance mechanisms across protocols', category: 'Compare' },
    ],
}

function SuggestedQuestions({ protocol, onSelect }) {
    const questions = SUGGESTIONS[protocol] || SUGGESTIONS.compare

    return (
        <div className="suggested-container">
            <p className="suggested-label">Try asking</p>
            <div className="suggested-grid">
                {questions.map((q, i) => (
                    <button
                        key={i}
                        className="suggested-card glass glass-hover animate-slide-up"
                        style={{ animationDelay: `${i * 0.1}s` }}
                        onClick={() => onSelect(q.text)}
                    >
                        <span className="suggested-category">{q.category}</span>
                        <span className="suggested-text">{q.text}</span>
                    </button>
                ))}
            </div>
        </div>
    )
}

export default SuggestedQuestions
