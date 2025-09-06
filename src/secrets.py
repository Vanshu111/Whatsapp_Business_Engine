import json, boto3, os
_secrets_cache = {}
def get_secret(name: str) -> dict:
    if name in _secrets_cache: return _secrets_cache[name]
    sm = boto3.client("secretsmanager")
    resp = sm.get_secret_value(SecretId=name)
    secret = json.loads(resp["SecretString"])
    _secrets_cache[name] = secret
    return secret

# usage:
# secrets = get_secret(os.getenv("SECRET_NAME_COMMON", "wabe/common"))
# TWILIO_AUTH_TOKEN = secrets["TWILIO_AUTH_TOKEN"]
# GEMINI_API_KEY    = secrets["GEMINI_API_KEY"]
