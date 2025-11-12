import json
import boto3
import os
import uuid

s3 = boto3.client('s3')
bucket_name = os.environ['UPLOAD_BUCKET']

def lambda_handler(event, context):
    try:
        # Get filename and content type from query parameters
        filename = None
        content_type = None
        
        if 'queryStringParameters' in event and event['queryStringParameters']:
            filename = event['queryStringParameters'].get('filename')
            content_type = event['queryStringParameters'].get('contentType', 'application/octet-stream')
        
        # Generate key with filename if provided, otherwise use UUID
        if filename:
            key = f"{uuid.uuid4()}_{filename}"
        else:
            key = str(uuid.uuid4())
        
        # Generate presigned URL with ContentType
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket_name,
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=3600,
            HttpMethod='PUT'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({'upload_url': url, 'file_key': key})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }