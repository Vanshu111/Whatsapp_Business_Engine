import boto3, os, datetime
from .errors import PersistenceError 
from ..models import ChatSummariesItem, ChatMemoryItem
from ..app_config import DDB_CHAT_SUMMARIES_TABLE, DDB_CHAT_MEMORY_TABLE

dynamodb = boto3.resource("dynamodb")
_summaries = dynamodb.Table(DDB_CHAT_SUMMARIES_TABLE)
_memory    = dynamodb.Table(DDB_CHAT_MEMORY_TABLE)

def load_active(session_id: str) -> dict:
    resp = _summaries.get_item(Key={"sessionId": session_id, "timestamp": "active_session"})
    return resp.get("Item", {})

def persist_active(item: ChatSummariesItem):
    _summaries.put_item(Item=item.dict())

def end_session(session_id: str, timestamp: str, active: dict, mem: ChatMemoryItem):
    _summaries.put_item(Item=ChatSummariesItem(**{**active, "timestamp": timestamp}).dict())
    _summaries.delete_item(Key={"sessionId": session_id, "timestamp": "active_session"})
    _memory.put_item(Item=mem.dict())
