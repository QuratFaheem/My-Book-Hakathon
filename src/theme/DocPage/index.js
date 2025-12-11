import React from 'react';
import ChatbotComponent from '@site/src/components/ChatbotComponent';

// A wrapper for documentation pages that adds the chatbot
const DocPageWithChatbot = (props) => {
  const { content: DocContent } = props;
  const { metadata } = DocContent;

  return (
    <>
      <DocContent />
      {/* Only show chatbot on documentation pages */}
      {metadata && metadata.permalink && metadata.permalink.startsWith('/docs') && (
        <ChatbotComponent />
      )}
    </>
  );
};

export default DocPageWithChatbot;