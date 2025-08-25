class MeetingScheduler {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
        this.init();
    }

    async init() {
        await this.loadUsers();
        await this.loadMessages();
        this.setupEventListeners();
    }

    async loadUsers() {
        try {
            const response = await fetch(`${this.baseURL}/users`);
            const data = await response.json();
            
            if (data.success) {
                const userSelect = document.getElementById('user-select');
                data.users.forEach(user => {
                    const option = document.createElement('option');
                    option.value = `${user.name}|${user.email}`;
                    option.textContent = user.name;
                    userSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }

    async loadMessages() {
        try {
            const response = await fetch(`${this.baseURL}/messages`);
            const data = await response.json();
            
            if (data.success) {
                this.displayMessages(data.messages);
            }
        } catch (error) {
            console.error('Error loading messages:', error);
            this.showStatus('Error loading messages. Make sure the backend is running.', 'error');
        }
    }

    displayMessages(messages) {
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = '';
        
        messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            
            const timestamp = new Date(message.timestamp).toLocaleString();
            
            messageDiv.innerHTML = `
                <div class="message-header">
                    <span class="user-name">${message.user_name}</span>
                    <span class="timestamp">${timestamp}</span>
                </div>
                <div class="message-content">${message.message}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
        });
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    setupEventListeners() {
        // Send message
        document.getElementById('send-btn').addEventListener('click', () => {
            this.sendMessage();
        });
        
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Schedule meeting
        document.getElementById('schedule-btn').addEventListener('click', () => {
            this.scheduleMeeting();
        });
    }

    async sendMessage() {
        const userSelect = document.getElementById('user-select');
        const messageInput = document.getElementById('message-input');
        
        const userValue = userSelect.value;
        const message = messageInput.value.trim();
        
        if (!userValue || !message) {
            this.showStatus('Please select a user and enter a message.', 'error');
            return;
        }
        
        const [userName, userEmail] = userValue.split('|');
        
        try {
            const response = await fetch(`${this.baseURL}/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_name: userName,
                    user_email: userEmail,
                    message: message
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                messageInput.value = '';
                await this.loadMessages();
                this.showStatus('Message sent successfully!', 'success');
            } else {
                this.showStatus(`Error: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.showStatus('Error sending message. Check connection.', 'error');
        }
    }

    async scheduleMeeting() {
        this.showStatus('🤖 Analyzing chat for meeting scheduling...', 'info');
        
        try {
            const response = await fetch(`${this.baseURL}/schedule-meeting`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                const meeting = data.meeting_details;
                const statusHTML = `
                    <h3>✅ Meeting Scheduled Successfully!</h3>
                    <p><strong>Title:</strong> ${meeting.title}</p>
                    <p><strong>Date:</strong> ${meeting.date}</p>
                    <p><strong>Time:</strong> ${meeting.time}</p>
                    <p><strong>Participants:</strong> ${meeting.participants.length} people</p>
                    <p><strong>📧 Confirmation emails sent to all participants!</strong></p>
                `;
                this.showStatus(statusHTML, 'success');
            } else if (data.needs_followup) {
                this.showStatus(`🤔 ${data.message}`, 'info');
            } else {
                this.showStatus(`❌ ${data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error scheduling meeting:', error);
            this.showStatus('Error scheduling meeting. Check connection.', 'error');
        }
    }

    showStatus(message, type) {
        const statusDiv = document.getElementById('status-messages');
        statusDiv.innerHTML = `<div class="${type}-message">${message}</div>`;
    }
}

// Initialize the application when page loads
document.addEventListener('DOMContentLoaded', () => {
    new MeetingScheduler();
});
