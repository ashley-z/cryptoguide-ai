import './ProtocolSelector.css'

function ProtocolSelector({
    protocols,
    selected,
    onChange,
    compareMode,
    compareProtocol,
    onCompareProtocolChange,
    onToggleCompare,
    availableCompareProtocols,
}) {
    return (
        <div className="protocol-selector">
            <select
                id="protocol-select"
                className="protocol-select"
                value={selected}
                onChange={(e) => onChange(e.target.value)}
            >
                {protocols.map((p) => (
                    <option key={p.id} value={p.id}>
                        {p.icon} {p.name}
                    </option>
                ))}
            </select>

            <button
                className={`compare-toggle ${compareMode ? 'compare-toggle-active' : ''}`}
                onClick={onToggleCompare}
                title={compareMode ? 'Switch to single protocol' : 'Compare protocols'}
            >
                ⚡ {compareMode ? 'Comparing' : 'Compare'}
            </button>

            {compareMode && (
                <>
                    <span className="compare-vs">vs</span>
                    <select
                        className="protocol-select protocol-select-compare"
                        value={compareProtocol}
                        onChange={(e) => onCompareProtocolChange(e.target.value)}
                    >
                        {availableCompareProtocols.map((p) => (
                            <option key={p.id} value={p.id}>
                                {p.icon} {p.name}
                            </option>
                        ))}
                    </select>
                </>
            )}
        </div>
    )
}

export default ProtocolSelector
