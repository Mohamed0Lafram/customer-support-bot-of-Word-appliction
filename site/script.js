class ChatApp {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.charCount = document.querySelector('.char-count');
        
        this.isTyping = false;
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.autoResizeTextarea();
        this.updateCharCount();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.messageInput.addEventListener('input', () => {
            this.autoResizeTextarea();
            this.updateCharCount();
            this.updateSendButton();
        });
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    updateCharCount() {
        const currentLength = this.messageInput.value.length;
        this.charCount.textContent = `${currentLength}/1000`;
        
        if (currentLength > 900) {
            this.charCount.style.color = '#dc3545';
        } else if (currentLength > 800) {
            this.charCount.style.color = '#ffc107';
        } else {
            this.charCount.style.color = '#6c757d';
        }
    }
    
    updateSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText;
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.autoResizeTextarea();
        this.updateCharCount();
        this.updateSendButton();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Simulate AI response delay
        await this.delay(1000 + Math.random() * 2000);
        
        // Remove typing indicator
        this.hideTypingIndicator();
        
        // Generate AI response
        
        const aiResponse = await this.generateAIResponse(message);
        this.addMessage(aiResponse, 'bot');
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const iconClass = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        const iconElement = sender === 'user' ? 'user-icon' : 'bot-icon';
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="${iconClass} ${iconElement}"></i>
                <div class="text">${this.escapeHtml(text)}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator-container';
        typingDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-robot bot-icon"></i>
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = this.chatMessages.querySelector('.typing-indicator-container');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
async generateAIResponse(userMessage) {
    try {
        const response = await fetch("http://127.0.0.1:8000/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: userMessage,
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("AI Response:", data);
        return data.response;
    } catch (error) {
        console.error("Error:", error);
        // Fallback responses when API is not available
        const fallbackResponses = [
            "I'm sorry, I'm having trouble connecting to my server right now. Please try again later.",
            "It looks like my connection is down. I'll be back online soon!",
            "I'm experiencing some technical difficulties. Please try again in a moment.",
            "Sorry, I can't access my knowledge base at the moment. Please try again later."
        ];
        return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
    }
}

    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the chat app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
}); 