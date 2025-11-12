import json
import boto3
import os

s3 = boto3.client('s3')
bucket = os.environ['ORGANIZED_BUCKET']

def lambda_handler(event, context):
    try:
        # List all objects recursively (including those in folders)
        result = s3.list_objects_v2(Bucket=bucket)
        files = []
        
        if 'Contents' in result:
            for obj in result['Contents']:
                # Skip folder markers (objects ending with /)
                if not obj['Key'].endswith('/'):
                    files.append({'key': obj['Key']})
        
        # Sort files by last modified date (newest first)
        files.sort(key=lambda x: x.get('LastModified', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({'files': files})
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