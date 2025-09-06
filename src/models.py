from pydantic import BaseModel, Field
from typing import List, Optional

class ChatSummariesItem(BaseModel):
    sessionId: str
    timestamp: str
    conversation: List[str] = Field(default_factory=list)
    chat_ended: bool = False
    user_role: str = "unknown"
    last_processed_message: str = ""
    processed_message_sids: List[str] = Field(default_factory=list)
    session_ended: bool = False
    state: str = "active"
    summary: str = ""
    summary_done: bool = False
    last_active: str = ""

class ChatMemoryItem(BaseModel):
    sessionId: str
    sender: str
    summary: str = ""
    name: Optional[str] = None
    location: Optional[str] = None
    contact_confirmed: bool = False
    device_ip: Optional[str] = None
