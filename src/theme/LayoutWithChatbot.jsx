import React from 'react';
import ChatbotComponent from '@site/src/components/ChatbotComponent';

// A wrapper component that adds the chatbot to textbook pages
const LayoutWithChatbot = ({ children, ...props }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <main style={{ flex: 1 }}>
        {children}
      </main>
      <div 
        style={{ 
          position: 'fixed', 
          bottom: '20px', 
          right: '20px', 
          width: '400px', 
          height: '500px',
          zIndex: 1000
        }}
      >
        <ChatbotComponent />
      </div>
    </div>
  );
};

export default LayoutWithChatbot;