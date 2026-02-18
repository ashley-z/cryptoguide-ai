import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import SourceCard from './SourceCard'
import './MessageBubble.css'

function MessageBubble({ message, index }) {
    const isUser = message.role === 'user'

    return (
        <div
            className={`message ${isUser ? 'message-user' : 'message-assistant'} animate-slide-up`}
            style={{ animationDelay: `${index * 0.05}s` }}
        >
            {isUser ? (
                <div className="message-user-content">
                    <p>{message.content}</p>
                </div>
            ) : (
                <div className={`message-ai-content ${message.isError ? 'message-error' : ''}`}>
                    <div className="ai-indicator">
                        <span className="ai-dot" />
                        <span className="ai-label">CryptoGuide AI</span>
                        {message.isComparison && (
                            <span className="ai-badge-compare">Comparison</span>
                        )}
                    </div>
                    <div className="prose-ai">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                    {message.isError && (
                        <button
                            className="retry-btn"
                            onClick={() => window.location.reload()}
                        >
                            ↻ Retry
                        </button>
                    )}
                    {message.sources && message.sources.length > 0 && (
                        <div className="sources-section">
                            <div className="sources-header">
                                <span className="sources-icon">📎</span>
                                <span className="sources-label">Sources ({message.sources.length})</span>
                            </div>
                            <div className="sources-list">
                                {message.sources.map((source, i) => (
                                    <SourceCard key={i} source={source} index={i} />
                                ))}
                            </div>
                        </div>
                    )}
                    {message.metadata && message.metadata.model_used && (
                        <div className="message-meta">
                            <span>Model: {message.metadata.model_used}</span>
                            {message.metadata.cost_usd && (
                                <span>Cost: ${message.metadata.cost_usd.toFixed(4)}</span>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default MessageBubble
