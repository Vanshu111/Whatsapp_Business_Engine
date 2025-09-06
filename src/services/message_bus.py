import boto3, json, os
from ..app_config import SQS_INBOUND_QUEUE_URL, SNS_ALERTS_TOPIC_ARN
sqs = boto3.client("sqs"); sns = boto3.client("sns")

def enqueue_inbound(payload: dict):
    sqs.send_message(QueueUrl=SQS_INBOUND_QUEUE_URL, MessageBody=json.dumps(payload))

def alert(topic: str, message: str):
    if SNS_ALERTS_TOPIC_ARN:
        sns.publish(TopicArn=SNS_ALERTS_TOPIC_ARN, Subject=topic, Message=message)
