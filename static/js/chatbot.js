document.addEventListener('DOMContentLoaded', function() {
    const chatbot = document.getElementById('ai-chatbot');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const chatForm = document.getElementById('chat-form');
    const chatToggle = document.getElementById('chat-toggle');

    if (chatToggle) {
        chatToggle.addEventListener('click', function() {
            chatbot.classList.toggle('collapsed');
        });
    }

    if (chatForm) {
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage('user', message);
            chatInput.value = '';

            // Show loading state
            addMessage('assistant', '...', 'loading-message');

            try {
                const response = await fetch('/ai/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                
                // Remove loading message and add AI response
                const loadingMsg = chatMessages.querySelector('.loading-message');
                if (loadingMsg) loadingMsg.remove();
                addMessage('assistant', data.response);
            } catch (error) {
                console.error('Error:', error);
                const loadingMsg = chatMessages.querySelector('.loading-message');
                if (loadingMsg) loadingMsg.remove();
                addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
            }
        });
    }

    function addMessage(role, content, className='') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role}-message ${className}`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
