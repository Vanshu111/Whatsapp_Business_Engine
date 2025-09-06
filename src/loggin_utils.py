import json, logging, os, time, uuid
logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO"))
log = logging.getLogger("wabe")

def ctx_log(event, **kw):
    base = {
        "request_id": str(uuid.uuid4()),
        "ts": int(time.time()),
        "event_type": "app",
    }
    base.update(kw)
    logging.getLogger("wabe").info(json.dumps(base))
