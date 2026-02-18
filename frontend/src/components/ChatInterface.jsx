import MessageBubble from './MessageBubble'
import LoadingState from './LoadingState'
import { useEffect, useRef } from 'react'
import './ChatInterface.css'

function ChatInterface({ messages, isLoading }) {
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, isLoading])

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.map((msg, i) => (
                    <MessageBubble
                        key={i}
                        message={msg}
                        index={i}
                    />
                ))}
                {isLoading && <LoadingState />}
                <div ref={bottomRef} />
            </div>
        </div>
    )
}

export default ChatInterface
