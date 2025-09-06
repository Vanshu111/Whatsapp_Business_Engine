import json, os, datetime
from .logging_utils import ctx_log, log
from .secrets import get_secret
from .app_config import SESSION_TIMEOUT
from .providers.llm_router import respond
from .services.session_store import load_active, persist_active, end_session
from .services.rag_service import RAGStore, build_prompt
from .services.reply_logic import infer_role_and_question, extract_key_details, summarize

rag = RAGStore()
secrets = get_secret(os.getenv("SECRET_NAME_COMMON","wabe/common"))

def lambda_handler(event, context):
    for rec in event["Records"]:
        msg = json.loads(rec["body"])
        user_msg = msg["user_msg"]; sender = msg["sender"]; message_sid = msg["message_sid"]
        session_id = sender.split(":")[-1]
        timestamp = datetime.datetime.utcnow().isoformat()

        item = load_active(session_id) or {
          "conversation":[], "key_details":{}, "processed_message_sids":[], "user_role":"unknown",
          "pending_question":None, "last_active": timestamp, "chat_ended": False,
          "session_ended": False, "state":"active", "summary":"", "summary_done": False,
        }

        # de-dupe
        if message_sid in item["processed_message_sids"]:
            continue
        item["processed_message_sids"] = (item["processed_message_sids"] + [message_sid])[-10:]
        item["conversation"] = (item["conversation"] + [user_msg])[-20:]
        item["last_active"] = timestamp

        # timeout
        try:
            last = datetime.datetime.fromisoformat(item["last_active"])
        except Exception:
            last = datetime.datetime.utcnow()
        if datetime.datetime.utcnow() - last > SESSION_TIMEOUT:
            item.update({"chat_ended": True, "session_ended": True, "state":"timeout_ended"})

        # slot filling or next question
        tailored_q = None
        pending = item.get("pending_question")
        if pending:
            item["key_details"], filled = extract_key_details(user_msg, pending, item.get("key_details",{}))
            if filled:
                item["pending_question"] = None
            else:
                tailored_q = {"name":"Could you share your name?",
                              "contact_confirmation":f"Is {sender} the correct number? (Reply 'yes')",
                              "location":"Where are you located?"}[pending]
        if not item.get("pending_question"):
            if not item["key_details"].get("name"):
                item["pending_question"] = "name"; tailored_q = "Could you share your name?"
            elif not item["key_details"].get("contact_confirmed"):
                item["pending_question"] = "contact_confirmation"; tailored_q = f"Is {sender} the correct number? (Reply 'yes')"
            elif not item["key_details"].get("location"):
                item["pending_question"] = "location"; tailored_q = "Where are you located?"
            else:
                role, nq = infer_role_and_question(lambda p: respond(p, secrets), user_msg, item["conversation"], item["user_role"])
                if role != "unknown": item["user_role"] = role
                if nq: tailored_q = nq

        # RAG
        context_docs = rag.search(user_msg, k=5)
        prompt = build_prompt(user_msg, context_docs)
        system = f"You are a business assistant for a {item['user_role']} user. Respond in 1–2 sentences and ask one follow-up."
        reply = respond(system + "\n\n" + prompt, secrets)
        if tailored_q and not reply.endswith(tailored_q):
            reply = f"{reply}\n{tailored_q}"

        # persist progress
        persist_active(item_model := type("X",(object,),item))
  

        # End-session keyword handling 
        if user_msg.lower().strip() in {"end chat","exit","quit","stop"} or item["chat_ended"]:
            summary = summarize(lambda p: respond(p, secrets), item["conversation"])
            item.update({"summary": summary, "summary_done": True, "session_ended": True, "chat_ended": True, "state":"ended"})
            # persist final
            end_session(session_id, timestamp, item, mem_model := type("Y",(object,),{
                "sessionId": session_id, "sender": sender, "summary": summary,
                "name": item["key_details"].get("name"),
                "location": item["key_details"].get("location"),
                "contact_confirmed": item["key_details"].get("contact_confirmed", False),
                "device_ip": None
            }))
