import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MeetingAgent:
    def __init__(self):
        self.days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.times = ['morning', 'afternoon', 'evening']
    
    def detect_meeting_intent(self, messages: List[Dict]) -> bool:
        """Detect if users want to schedule a meeting"""
        meeting_keywords = ['meeting', 'schedule', 'call', 'discuss', 'get together', 'appointment']
        
        for msg in messages:
            message_lower = msg['message'].lower()
            if any(keyword in message_lower for keyword in meeting_keywords):
                return True
        return False
    
    def extract_availability(self, messages: List[Dict]) -> Dict[str, List[str]]:
        """Extract availability from chat messages"""
        availability = {}
        
        for msg in messages:
            user_email = msg['user_email']
            message = msg['message'].lower()
            
            if user_email not in availability:
                availability[user_email] = []
            
            # Look for day mentions
            for day in self.days:
                if day in message:
                    # Look for time mentions
                    for time_slot in self.times:
                        if time_slot in message:
                            slot = f"{day} {time_slot}"
                            if slot not in availability[user_email]:
                                availability[user_email].append(slot)
                    
                    # If day mentioned without specific time, assume whole day
                    if not any(time_slot in message for time_slot in self.times):
                        for time_slot in self.times:
                            slot = f"{day} {time_slot}"
                            if slot not in availability[user_email]:
                                availability[user_email].append(slot)
        
        return availability
    
    def find_common_time(self, availability: Dict[str, List[str]]) -> Optional[str]:
        """Find common available time slot"""
        if not availability:
            return None
        
        all_slots = set()
        for user_slots in availability.values():
            all_slots.update(user_slots)
        
        # Count how many users are available for each slot
        slot_counts = {}
        for slot in all_slots:
            count = sum(1 for user_slots in availability.values() if slot in user_slots)
            slot_counts[slot] = count
        
        # Find slot with majority agreement (more than half of users)
        total_users = len(availability)
        majority_threshold = total_users / 2
        
        best_slot = None
        max_count = 0
        
        for slot, count in slot_counts.items():
            if count > majority_threshold and count > max_count:
                best_slot = slot
                max_count = count
        
        return best_slot
    
    def schedule_meeting(self, messages: List[Dict]) -> Dict:
        """Main function to schedule meeting from chat"""
        result = {
            'success': False,
            'message': '',
            'meeting_details': None,
            'needs_followup': False
        }
        
        # Check if meeting intent exists
        if not self.detect_meeting_intent(messages):
            result['message'] = "No meeting scheduling intent detected in the chat."
            return result
        
        # Extract availability
        availability = self.extract_availability(messages)
        
        if not availability:
            result['needs_followup'] = True
            result['message'] = "Could you please share your availability? For example: 'I'm available Tuesday afternoon' or 'Monday to Wednesday works for me'"
            return result
        
        # Find common time
        common_time = self.find_common_time(availability)
        
        if not common_time:
            result['needs_followup'] = True
            result['message'] = f"I found these availabilities: {availability}. Could you find a common time that works for everyone?"
            return result
        
        # Calculate actual date (next occurrence of the day)
        day_name, time_slot = common_time.split(' ', 1)
        meeting_date = self.get_next_date(day_name)
        meeting_time = self.get_time_from_slot(time_slot)
        
        result['success'] = True
        result['message'] = f"Great! I've scheduled a meeting for {common_time.title()}."
        result['meeting_details'] = {
            'title': 'Team Meeting',
            'date': meeting_date,
            'time': meeting_time,
            'participants': list(availability.keys())
        }
        
        return result
    
    def get_next_date(self, day_name: str) -> str:
        """Get next occurrence of a day"""
        today = datetime.now()
        days_ahead = self.days.index(day_name.lower()) - today.weekday()
        
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        
        target_date = today + timedelta(days_ahead)
        return target_date.strftime('%Y-%m-%d')
    
    def get_time_from_slot(self, time_slot: str) -> str:
        """Convert time slot to actual time"""
        time_mapping = {
            'morning': '09:00',
            'afternoon': '14:00',
            'evening': '18:00'
        }
        return time_mapping.get(time_slot.lower(), '14:00')
    
    def send_confirmation_email(self, meeting_details: Dict, participant_emails: List[str]):
        """Send confirmation email to participants"""
        # Simple email simulation (in real app, configure SMTP)
        try:
            subject = f"Meeting Confirmation: {meeting_details['title']}"
            body = f"""
            Hello!
            
            Your meeting has been scheduled:
            
            Title: {meeting_details['title']}
            Date: {meeting_details['date']}
            Time: {meeting_details['time']}
            Participants: {', '.join(participant_emails)}
            
            Best regards,
            Meeting Scheduler Bot
            """
            
            print(f"📧 EMAIL SENT TO: {', '.join(participant_emails)}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            print("-" * 50)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
