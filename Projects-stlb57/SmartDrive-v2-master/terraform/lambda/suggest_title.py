import os
import json
import boto3
import urllib.request
import urllib.error

# This API token should be stored securely, e.g., in AWS Secrets Manager
# For now, we'll get it from an environment variable.
HF_API_TOKEN = os.environ['HF_API_TOKEN'] 
HF_MODEL = "facebook/bart-large-cnn" # This model works well for titles too

s3 = boto3.client('s3')
bucket = os.environ['ORGANIZED_BUCKET']

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

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        key = body.get('key')
        if not key:
            return cors_response(400, {"error": "Missing 'key' in request body"})

        # Get file content from S3
        obj = s3.get_object(Bucket=bucket, Key=key)
        # Use a sensible character limit for title generation
        content = obj['Body'].read().decode("utf-8", errors="ignore")[:1500] 

        # Call Hugging Face API
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        # Ask for a very short summary to act as a title
        payload = {"inputs": content, "parameters": {"max_length": 12, "min_length": 3}}

        request_data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=request_data, headers=headers, method="POST")

        with urllib.request.urlopen(request, timeout=30) as response:
            hf_text = response.read().decode("utf-8", errors="ignore")
        
        data = json.loads(hf_text)

        if isinstance(data, dict) and "error" in data:
            return cors_response(500, {"error": data["error"]})
            
        suggested_title = data[0]['summary_text']
        
        return cors_response(200, {'suggested_title': suggested_title.strip()})

    except Exception as e:
        print("ERROR:", str(e))
        return cors_response(500, {"error": str(e)})