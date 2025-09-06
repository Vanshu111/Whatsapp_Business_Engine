import jwt, os
from jwt import PyJWKClient

OKTA_ISSUER   = os.getenv("OKTA_ISSUER")
OKTA_AUDIENCE = os.getenv("OKTA_AUDIENCE")

_jwk_client = PyJWKClient(f"{OKTA_ISSUER}/v1/keys")

def validate_authorization(headers: dict) -> dict:
    auth = headers.get("Authorization","")
    if not auth.startswith("Bearer "): raise PermissionError("Missing bearer token")
    token = auth.split(" ",1)[1]
    signing_key = _jwk_client.get_signing_key_from_jwt(token).key
    claims = jwt.decode(token, signing_key, algorithms=["RS256"], audience=OKTA_AUDIENCE, issuer=OKTA_ISSUER)
    return claims  # contains sub, email, etc.
