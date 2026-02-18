import './LoadingState.css'

function LoadingState() {
    return (
        <div className="loading-container animate-fade-in">
            <div className="ai-indicator">
                <span className="ai-dot loading-pulse" />
                <span className="ai-label">CryptoGuide AI</span>
            </div>
            <div className="loading-lines">
                <div className="loading-line shimmer" style={{ width: '90%' }} />
                <div className="loading-line shimmer" style={{ width: '75%', animationDelay: '0.1s' }} />
                <div className="loading-line shimmer" style={{ width: '60%', animationDelay: '0.2s' }} />
            </div>
        </div>
    )
}

export default LoadingState
