import { useState } from 'react'
import './SourceCard.css'

function SourceCard({ source, index }) {
    const [expanded, setExpanded] = useState(false)

    return (
        <div
            className={`source-card glass ${expanded ? 'source-card-expanded' : ''}`}
            onClick={() => setExpanded(!expanded)}
        >
            <div className="source-card-header">
                <span className="source-index">[{source.id || index + 1}]</span>
                {source.protocol && (
                    <span className={`source-protocol-badge protocol-${source.protocol}`}>
                        {source.protocol}
                    </span>
                )}
                <span className="source-doc">{source.document}</span>
                {source.page && source.page !== 'N/A' && (
                    <span className="source-page">p. {source.page}</span>
                )}
                <span className={`source-chevron ${expanded ? 'expanded' : ''}`}>▸</span>
            </div>
            {expanded && (
                <div className="source-card-body animate-fade-in">
                    <p className="source-excerpt">{source.text || source.excerpt}</p>
                </div>
            )}
        </div>
    )
}

export default SourceCard
