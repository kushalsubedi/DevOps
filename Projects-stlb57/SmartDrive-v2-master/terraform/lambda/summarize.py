# import requests, os, json, boto3

# HF_API_TOKEN = os.environ['HF_API_TOKEN']  # Store in Lambda env vars
# HF_MODEL = "facebook/bart-large-cnn"

# s3 = boto3.client('s3')
# bucket = os.environ['BUCKET']

# def lambda_handler(event, context):
#     try:
#         if event.get("httpMethod") == "OPTIONS":
#             return {
#                 'statusCode': 200,
#                 'headers': {
#                     'Access-Control-Allow-Origin': '*',
#                     'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
#                     'Access-Control-Allow-Headers': '*'
#                 },
#                 'body': ''
#             }

#         body = json.loads(event['body'])
#         key = body['key']

#         obj = s3.get_object(Bucket=bucket, Key=key)
#         content = obj['Body'].read().decode('utf-8')[:2000]

#         headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
#         payload = {"inputs": content, "parameters": {"max_length": 100, "min_length": 30}}

#         response = requests.post(
#             f"https://api-inference.huggingface.co/models/{HF_MODEL}",
#             headers=headers, json=payload
#         )
#         response.raise_for_status()

#         data = response.json()
#         summary = data[0]['summary_text']

#         return {
#             'statusCode': 200,
#             'headers': {
#                 'Access-Control-Allow-Origin': '*',
#                 'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
#                 'Access-Control-Allow-Headers': '*'
#             },
#             'body': json.dumps({'summary': summary.strip()})
#         }

#     except Exception as e:
#         return {
#             'statusCode': 500,
#             'headers': {
#                 'Access-Control-Allow-Origin': '*',
#                 'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
#                 'Access-Control-Allow-Headers': '*'
#             },
#             'body': json.dumps({'error': str(e)})
#         }


# def lambda_handler(event, context):
#     body = json.loads(event['body'])
#     key = body['key']

#     obj = s3.get_object(Bucket=bucket, Key=key)
#     content = obj['Body'].read().decode('utf-8')[:2000]

#     headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
#     payload = {"inputs": content, "parameters": {"max_length": 100, "min_length": 30}}

#     response = requests.post(
#         f"https://api-inference.huggingface.co/models/{HF_MODEL}",
#         headers=headers, json=payload
#     )

#     summary = response.json()[0]['summary_text']
#     return {
#         'statusCode': 200,
#         'headers': {
#     'Access-Control-Allow-Origin': '*',
#     'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
#     'Access-Control-Allow-Headers': '*'
# },
#         'body': json.dumps({'summary': summary.strip()})
#     }


import os
import json
import boto3
import mimetypes
import urllib.request
import urllib.error

HF_API_TOKEN = os.environ['HF_API_TOKEN']
HF_MODEL = "facebook/bart-large-cnn"

s3 = boto3.client('s3')
bucket = os.environ['BUCKET']

def lambda_handler(event, context):
    try:
        print("EVENT:", json.dumps(event))

        # Handle CORS preflight request
        if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
            return cors_response(200, "")

        # Parse request body
        body = event.get('body', {})
        if isinstance(body, str):
            body = json.loads(body)

        key = body.get('key')
        if not key:
            return cors_response(400, {"error": "Missing 'key' in request body"})

        print(f"Processing key: {key}")

        # Get file from S3
        obj = s3.get_object(Bucket=bucket, Key=key)
        raw_bytes = obj['Body'].read()

        # Detect content type
        content_type, _ = mimetypes.guess_type(key)
        if content_type is None:
            content_type = obj.get('ContentType', 'application/octet-stream')

        # Extract text depending on file type
        if content_type.startswith("text/"):
            content = raw_bytes.decode("utf-8", errors="ignore")[:2000]
        else:
            return cors_response(400, {"error": f"Unsupported file type: {content_type}"})

        # Call Hugging Face API using stdlib (no external deps)
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": content, "parameters": {"max_length": 100, "min_length": 30}}

        request_data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=request_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                hf_status = response.getcode()
                hf_text = response.read().decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            hf_status = e.code
            hf_text = e.read().decode("utf-8", errors="ignore")
        except Exception as e:
            print("HF request error:", str(e))
            return cors_response(500, {"error": f"Failed to call summarization model: {str(e)}"})

        print("HF status:", hf_status, "Response:", hf_text)

        try:
            data = json.loads(hf_text)
        except json.JSONDecodeError:
            return cors_response(500, {"error": "Invalid response from summarization service"})

        # Handle HF errors
        if isinstance(data, dict) and "error" in data:
            return cors_response(500, {"error": data["error"]})

        summary = None
        if isinstance(data, dict) and "summary_text" in data:
            summary = data["summary_text"]
        elif isinstance(data, list) and data and isinstance(data[0], dict) and "summary_text" in data[0]:
            summary = data[0]["summary_text"]

        if not summary:
            return cors_response(500, {"error": "No summary returned by model"})

        return cors_response(200, {"summary": summary.strip()})

    except Exception as e:
        print("ERROR:", str(e))
        return cors_response(500, {"error": str(e)})


def cors_response(status_code, body):
    """Helper to attach CORS headers"""
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps(body) if not isinstance(body, str) else body
    }
