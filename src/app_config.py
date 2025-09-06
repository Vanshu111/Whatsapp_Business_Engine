import os
from datetime import timedelta

SESSION_TIMEOUT_MIN = int(os.getenv("SESSION_TIMEOUT_MIN", "30"))
SESSION_TIMEOUT = timedelta(minutes=SESSION_TIMEOUT_MIN)

# tables/queues/topics
DDB_CHAT_SUMMARIES_TABLE = os.getenv("DDB_CHAT_SUMMARIES_TABLE", "ChatSummaries")
DDB_CHAT_MEMORY_TABLE    = os.getenv("DDB_CHAT_MEMORY_TABLE", "ChatMemory")
SQS_INBOUND_QUEUE_URL    = os.getenv("SQS_INBOUND_QUEUE_URL")
SNS_ALERTS_TOPIC_ARN     = os.getenv("SNS_ALERTS_TOPIC_ARN")

# twilio
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER", "whatsapp:+14155238886")

# okta
OKTA_ISSUER   = os.getenv("OKTA_ISSUER")   # e.g., https://dev-xxx.okta.com/oauth2/default
OKTA_AUDIENCE = os.getenv("OKTA_AUDIENCE") # API GW authorizer audience (optional validation in code)
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID") # API GW authorizer client ID (optional validation in code)