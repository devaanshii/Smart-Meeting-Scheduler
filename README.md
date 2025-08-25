# AI Smart Meeting Scheduler 🤖

An intelligent meeting scheduler that analyzes team chat conversations and automatically schedules meetings based on participant availability. The system uses natural language processing to detect meeting intent and extract availability information from chat messages.

## Features

- **Smart Chat Analysis**: Automatically detects when team members want to schedule a meeting
- **Availability Extraction**: Parses natural language to understand when people are available
- **Intelligent Scheduling**: Finds common time slots that work for all participants
- **Email Notifications**: Sends confirmation emails to all meeting participants
- **Real-time Chat Interface**: Interactive web-based chat system
- **Database Integration**: Stores users, messages, and meeting details

## echnologies Used

### Backend
- **Flask**: Web framework for Python
- **SQLite**: Lightweight database for data storage
- **Flask-CORS**: Cross-Origin Resource Sharing support

### Frontend
- **HTML5**: Modern web markup
- **CSS3**: Responsive styling with gradients and animations
- **JavaScript**: Interactive functionality and API communication

### AI/NLP Components
- **Natural Language Processing**: Custom algorithm for intent detection
- **Availability Parsing**: Pattern matching for time and date extraction
- **Smart Scheduling Logic**: Algorithm to find optimal meeting times

## Project Structure

```
ai-meeting-scheduler/
├── app.py                 # Main Flask application
├── database.py            # Database management and operations
├── meeting_agent.py       # AI agent for meeting scheduling logic
├── index.html            # Frontend interface
├── style.css             # Styling and responsive design
├── script.js             # Frontend JavaScript functionality
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-meeting-scheduler.git
   cd ai-meeting-scheduler
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## How to Use

### Getting Started
1. Launch the application and open it in your web browser
2. The system comes pre-loaded with sample users and conversations
3. You can add new messages by selecting a user and typing a message

### Scheduling a Meeting
1. **Chat naturally** about wanting to schedule a meeting
2. **Share availability** using natural language like:
   - "I'm available Tuesday afternoon"
   - "Monday to Wednesday works for me"
   - "I can do morning meetings this week"
3. **Click "Schedule Meeting"** to let the AI analyze the conversation
4. The system will automatically find common availability and schedule the meeting

### Example Conversation
```
Alice: "Hey team, we should schedule a meeting to discuss the project"
Bob: "Great idea! I'm available Monday to Wednesday"
Carol: "Tuesday afternoon works best for me"
Alice: "Tuesday afternoon is perfect for me too"
```

After clicking "Schedule Meeting", the AI will:
- Detect the meeting intent
- Extract that Bob is available Mon-Wed, Carol prefers Tue afternoon, Alice agrees with Tue afternoon
- Schedule a meeting for Tuesday afternoon
- Send confirmation emails to all participants

## 🧠 AI Features Explained

### Meeting Intent Detection
The system recognizes various ways people express wanting to meet:
- "Let's schedule a meeting"
- "We should have a call"
- "Can we get together to discuss..."
- "Let's set up an appointment"

### Availability Parsing
Understands natural language time expressions:
- **Days**: Monday, Tuesday, Wednesday, etc.
- **Time periods**: morning, afternoon, evening
- **Ranges**: "Monday to Wednesday", "next week"
- **Preferences**: "works for me", "I'm available", "I can do"

### Smart Scheduling Algorithm
- Finds overlapping availability among all participants
- Uses majority voting when perfect consensus isn't available
- Calculates actual dates (next occurrence of mentioned days)
- Converts time slots to specific times (morning = 9:00 AM, etc.)

## 📊 Database Schema

### Users Table
- `id`: Unique identifier
- `name`: User's full name
- `email`: Email address
- `created_at`: Registration timestamp

### Messages Table
- `id`: Message identifier
- `user_id`: Foreign key to users table
- `message`: Message content
- `timestamp`: When message was sent

### Meetings Table
- `id`: Meeting identifier
- `title`: Meeting title
- `date`: Meeting date (YYYY-MM-DD)
- `time`: Meeting time (HH:MM)
- `participants`: Comma-separated list of participant emails
- `created_at`: When meeting was scheduled

## UI/UX Features

- **Responsive Design**: Works on desktop and mobile devices
- **Modern Interface**: Clean, professional design with gradients
- **Real-time Updates**: Chat messages appear instantly
- **Status Notifications**: Clear feedback for all actions
- **Intuitive Controls**: Easy-to-use chat interface

## 🔧 API Endpoints

### GET `/api/messages`
Retrieve all chat messages with user information

### POST `/api/messages`
Add a new message to the chat
```json
{
  "user_name": "Alice Johnson",
  "user_email": "alice@email.com",
  "message": "Let's schedule a meeting!"
}
```

### POST `/api/schedule-meeting`
Analyze chat and schedule a meeting based on conversation

### GET `/api/users`
Retrieve all registered users

## Future Enhancements

- **Calendar Integration**: Sync with Google Calendar, Outlook
- **Advanced NLP**: More sophisticated language understanding
- **Time Zone Support**: Handle participants in different time zones
- **Conflict Detection**: Check for scheduling conflicts
- **Meeting Reminders**: Automated reminder system
- **Video Conferencing**: Integration with Zoom, Teams, etc.
- **Mobile App**: Native iOS and Android applications

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License

## 👥 Authors

- **Devanshi Mathan** - https://github.com/devaanshii

## Acknowledgments

- Thanks to the Flask community for excellent documentation
- Inspired by modern AI-powered productivity tools
- Built with ❤️ for better team collaboration