import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import { translate } from '@docusaurus/Translate';

const ChatbotComponent = ({ className = '' }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);
  const location = useLocation();

  // Initialize session on component mount
  useEffect(() => {
    // Try to restore session from localStorage
    const savedSessionId = localStorage.getItem('textbook-chat-session-id');
    const savedMessages = localStorage.getItem('textbook-chat-messages');

    if (savedSessionId) {
      setSessionId(savedSessionId);
    }

    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (e) {
        console.error('Error parsing saved messages:', e);
      }
    }

    // If no session exists, create one
    if (!savedSessionId) {
      const initSession = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/chat/session', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              initial_message: translate({
                id: 'chatbot.welcome.message',
                message: 'Hello, I am ready to help you with questions about the Physical AI & Humanoid Robotics textbook.'
              })
            })
          });

          const data = await response.json();
          setSessionId(data.session_id);
          localStorage.setItem('textbook-chat-session-id', data.session_id);
        } catch (error) {
          console.error('Error initializing chat session:', error);
        }
      };

      initSession();
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('textbook-chat-messages', JSON.stringify(messages));
    }
  }, [messages]);

  // Save session ID to localStorage whenever it changes
  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('textbook-chat-session-id', sessionId);
    }
  }, [sessionId]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get response from the backend
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          session_id: sessionId,
          context: {
            current_page: location.pathname,
            course: 'physical-ai-humanoid-robotics'
          }
        })
      });

      const data = await response.json();

      // Add assistant response to the chat
      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        sources: data.sources,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSessionId(data.session_id); // Update session ID if it changed
    } catch (error) {
      console.error('Error getting chat response:', error);

      // Add error message to the chat
      const errorMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: translate({
          id: 'chatbot.error.message',
          message: 'Sorry, I encountered an error processing your request. Please try again.'
        }),
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const clearChatHistory = () => {
    setMessages([]);
    localStorage.removeItem('textbook-chat-messages');
  };

  if (!isOpen) {
    return (
      <div className={`chatbot-toggle-container ${className}`} style={{ position: 'fixed', bottom: '20px', right: '20px', zIndex: 1000 }}>
        <button
          onClick={toggleChat}
          style={{
            padding: '15px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            cursor: 'pointer',
            fontSize: '20px',
            width: '60px',
            height: '60px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
          }}
          title={translate({ id: 'chatbot.toggle.title', message: 'Open chat' })}
        >
          💬
        </button>
      </div>
    );
  }

  return (
    <div className={`chatbot-container ${className}`} style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '400px',
      height: '500px',
      zIndex: 1000,
      border: '1px solid #ddd',
      borderRadius: '8px',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: 'white',
      boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: '#f8f9fa',
        padding: '10px 15px',
        borderBottom: '1px solid #ddd'
      }}>
        <h3 style={{ margin: 0, fontSize: '1rem' }}>
          {translate({ id: 'chatbot.title', message: 'Textbook Assistant' })}
        </h3>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={clearChatHistory}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1rem',
              cursor: 'pointer',
              padding: '0 5px',
              color: '#6c757d'
            }}
            title={translate({ id: 'chatbot.clear.title', message: 'Clear chat history' })}
          >
            🗑️
          </button>
          <button
            onClick={toggleChat}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.2rem',
              cursor: 'pointer',
              padding: '0',
              width: '30px',
              height: '30px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
            title={translate({ id: 'chatbot.close.title', message: 'Close chat' })}
          >
            ×
          </button>
        </div>
      </div>

      <div style={{
        flex: 1,
        padding: '15px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
            style={{
              display: 'flex',
              justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
              marginBottom: '10px'
            }}
          >
            <div
              style={{
                padding: '10px 15px',
                borderRadius: message.role === 'user' ? '18px 18px 0 18px' : '18px 18px 18px 0',
                maxWidth: '80%',
                backgroundColor: message.role === 'user' ? '#007bff' : '#f1f0f0',
                color: message.role === 'user' ? 'white' : 'black',
                wordWrap: 'break-word'
              }}
            >
              {message.content}
              {message.sources && message.sources.length > 0 && (
                <div style={{ marginTop: '8px', fontSize: '0.8em' }}>
                  <strong>{translate({ id: 'chatbot.sources.label', message: 'Sources:' })}</strong>
                  {message.sources.map((source, index) => (
                    <div key={index} style={{ marginLeft: '10px' }}>
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: '#007bff', textDecoration: 'none' }}
                      >
                        {source.title}
                      </a> (relevance: {(source.relevance_score * 100).toFixed(1)}%)
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div
            className="message assistant"
            style={{
              display: 'flex',
              justifyContent: 'flex-start',
              marginBottom: '10px'
            }}
          >
            <div
              style={{
                padding: '10px 15px',
                borderRadius: '18px 18px 18px 0',
                backgroundColor: '#f1f0f0',
                color: 'black'
              }}
            >
              {translate({ id: 'chatbot.thinking', message: 'Thinking...' })}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} style={{
        display: 'flex',
        padding: '15px',
        borderTop: '1px solid #ddd',
        backgroundColor: '#f8f9fa'
      }}>
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={translate({
            id: 'chatbot.input.placeholder',
            message: 'Ask a question about this chapter...'
          })}
          disabled={isLoading}
          rows={2}
          style={{
            flex: 1,
            padding: '10px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            resize: 'vertical',
            minHeight: '40px',
            maxHeight: '100px',
            marginRight: '10px'
          }}
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          style={{
            padding: '10px 15px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: (!inputValue.trim() || isLoading) ? 'not-allowed' : 'pointer',
            opacity: (!inputValue.trim() || isLoading) ? 0.6 : 1
          }}
        >
          {translate({ id: 'chatbot.send.button', message: 'Send' })}
        </button>
      </form>
    </div>
  );
};

export default ChatbotComponent;