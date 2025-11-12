import json
import boto3
import os

s3 = boto3.client('s3')
bucket = os.environ['ORGANIZED_BUCKET']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    old_key = body['old_key']
    new_key = body['new_key']

    # Check for collision
    try:
        s3.head_object(Bucket=bucket, Key=new_key)
        return {
            'statusCode': 409,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'File with new name already exists'})
        }
    except s3.exceptions.ClientError:
        pass

    s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': old_key}, Key=new_key)
    s3.delete_object(Bucket=bucket, Key=old_key)

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'new_key': new_key})
    }
