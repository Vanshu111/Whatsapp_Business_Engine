import boto3, json
bedrock = boto3.client("bedrock-runtime")

def claude_haiku_chat(prompt: str, max_tokens=200):
    body = {
      "anthropic_version": "bedrock-2023-05-31",
      "messages": [{"role":"user","content":[{"type":"text","text":prompt}]}],
      "max_tokens": max_tokens,
      "temperature": 0.7
    }
    resp = bedrock.invoke_model(modelId="anthropic.claude-3-haiku-20240307-v1:0",
                                body=json.dumps(body))
    out = json.loads(resp["body"].read())
    return out["content"][0]["text"]
