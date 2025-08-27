import uuid
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from config import Config

@dataclass
class ConversationEntry:
    user_message: str
    assistant_response: str
    timestamp: float
    context_used: List[str]  # Citations used in the response

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, List[ConversationEntry]] = {}
        self.session_timestamps: Dict[str, float] = {}
    
    def create_session(self) -> str:
        """
        Create a new session and return session ID
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        self.session_timestamps[session_id] = time.time()
        return session_id
    
    def add_conversation(self, session_id: str, user_message: str, 
                        assistant_response: str, context_used: List[str] = None):
        """
        Add a conversation entry to the session
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        entry = ConversationEntry(
            user_message=user_message,
            assistant_response=assistant_response,
            timestamp=time.time(),
            context_used=context_used or []
        )
        
        self.sessions[session_id].append(entry)
        self.session_timestamps[session_id] = time.time()
        
        # Keep only the last N conversations to manage memory
        if len(self.sessions[session_id]) > Config.MAX_CONVERSATION_HISTORY:
            self.sessions[session_id] = self.sessions[session_id][-Config.MAX_CONVERSATION_HISTORY:]
    
    def get_conversation_history(self, session_id: str, limit: int = None) -> List[Dict[str, str]]:
        """
        Get conversation history for a session
        Returns list of dictionaries with 'user' and 'assistant' keys
        """
        if session_id not in self.sessions:
            return []
        
        conversations = self.sessions[session_id]
        if limit:
            conversations = conversations[-limit:]
        
        return [
            {
                'user': entry.user_message,
                'assistant': entry.assistant_response,
                'timestamp': entry.timestamp,
                'citations': entry.context_used
            }
            for entry in conversations
        ]
    
    def get_recent_context(self, session_id: str, limit: int = 3) -> str:
        """
        Get recent conversation context as a formatted string
        """
        if session_id not in self.sessions:
            return ""
        
        recent_conversations = self.sessions[session_id][-limit:]
        
        context_parts = []
        for entry in recent_conversations:
            context_parts.append(f"User: {entry.user_message}")
            context_parts.append(f"Assistant: {entry.assistant_response[:200]}...")  # Truncate for context
        
        return "\n".join(context_parts)
    
    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists
        """
        return session_id in self.sessions
    
    def get_session_stats(self, session_id: str) -> Dict[str, any]:
        """
        Get statistics for a session
        """
        if session_id not in self.sessions:
            return {}
        
        conversations = self.sessions[session_id]
        
        return {
            'session_id': session_id,
            'total_conversations': len(conversations),
            'created_at': self.session_timestamps.get(session_id, 0),
            'last_activity': conversations[-1].timestamp if conversations else 0,
            'unique_citations': len(set(
                citation 
                for entry in conversations 
                for citation in entry.context_used
            ))
        }
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """
        Remove sessions older than specified hours
        """
        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)
        
        sessions_to_remove = [
            session_id for session_id, timestamp in self.session_timestamps.items()
            if timestamp < cutoff_time
        ]
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
            del self.session_timestamps[session_id]
        
        return len(sessions_to_remove)
    
    def export_session(self, session_id: str) -> Dict[str, any]:
        """
        Export session data for backup or analysis
        """
        if session_id not in self.sessions:
            return {}
        
        return {
            'session_id': session_id,
            'created_at': self.session_timestamps.get(session_id, 0),
            'conversations': [asdict(entry) for entry in self.sessions[session_id]]
        }
    
    def get_all_sessions(self) -> List[str]:
        """
        Get list of all active session IDs
        """
        return list(self.sessions.keys())
    
    def clear_session(self, session_id: str):
        """
        Clear all conversations in a session
        """
        if session_id in self.sessions:
            self.sessions[session_id] = []
            self.session_timestamps[session_id] = time.time()