import json
import boto3
import os
import mimetypes

s3 = boto3.client('s3')
bucket = os.environ['ORGANIZED_BUCKET']

def lambda_handler(event, context):
    result = s3.list_objects_v2(Bucket=bucket)
    files = result.get('Contents', [])

    total_size = sum(f['Size'] for f in files)
    mime_counts = {}

    for f in files:
        mime, _ = mimetypes.guess_type(f['Key'])
        category = (mime or "other").split('/')[0]
        mime_counts[category] = mime_counts.get(category, 0) + 1

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'file_count': len(files),
            'total_size_bytes': total_size,
            'type_distribution': mime_counts
        })
    }
