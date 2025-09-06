import base64, urllib.parse, json, os
from .logging_utils import ctx_log
from .auth_okta import validate_authorization
from .services.message_bus import enqueue_inbound

def lambda_handler(event, context):
    headers = event.get("headers", {})
    try:
        validate_authorization(headers)   # Okta JWT (API GW already checks—this is extra)
    except Exception:
        return {"statusCode": 401, "body": "Unauthorized"}

    raw_body = event.get("body","")
    if event.get("isBase64Encoded"): raw_body = base64.b64decode(raw_body).decode("utf-8")
    body = {k: v[0] for k, v in urllib.parse.parse_qs(raw_body).items()} if raw_body else {}
    user_msg   = body.get("Body"); sender = body.get("From"); msg_sid = body.get("MessageSid","")

    if not user_msg or not sender:
        return {"statusCode": 400, "body": json.dumps({"error":"Missing Body/From"})}

    enqueue_inbound({"user_msg": user_msg, "sender": sender, "message_sid": msg_sid, "headers": headers})
    ctx_log(event, action="ingress_enqueued", from_=sender)
    # Fast 200 back to Twilio
    return {"statusCode": 200, "body": "Accepted"}
