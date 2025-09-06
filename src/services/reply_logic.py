import re, json
from typing import Tuple, Optional
def infer_role_and_question(llm, user_msg: str, convo: list, current_role: str) -> Tuple[str, Optional[str]]:
    prompt = (
      "You are a business assistant. Return JSON only: "
      '{"role":"<role>","question":"<one_next_question_or_null>"}\n'
      f"History: {convo[-10:]}\nUser: {user_msg}"
    )
    try:
        ans = llm(prompt)
        data = json.loads(ans) if ans.strip().startswith("{") else {}
        return data.get("role", current_role or "unknown"), data.get("question")
    except Exception:
        return current_role or "unknown", None

def extract_key_details(user_msg: str, pending: Optional[str], state: dict) -> Tuple[dict, bool]:
    updated, filled = dict(state), False
    if pending == "name":
        m = re.search(r'(?:my name is|i am|call me)\s+([a-zA-Z ]{2,})', user_msg, re.I)#regex to find name
        if m: updated["name"] = m.group(1).strip().title(); filled = True
    elif pending == "contact_confirmation":
        if any(w in user_msg.lower() for w in ("yes","yep","yeah","correct")):
            updated["contact_confirmed"] = True; filled = True
    elif pending == "location":
        updated["location"] = user_msg.strip().title(); filled = True
    return updated, filled

def summarize(llm, convo: list) -> str:
    return llm("Summarize in 1–2 sentences with user role/name/location if known.\n" + "\n".join(convo[-20:]))
