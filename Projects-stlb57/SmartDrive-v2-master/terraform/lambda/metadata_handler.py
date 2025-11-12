import json
import boto3
import os
import mimetypes

s3 = boto3.client('s3')
destination_bucket = os.environ['ORGANIZED_BUCKET']

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            source_bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            # Determine content type from file extension
            content_type, _ = mimetypes.guess_type(key)
            content_type = (content_type or "others").split('/')[0]
         
            # Create new key with content type folder
            new_key = f"{content_type}/{key}"
            
            # Copy object to organized bucket
            s3.copy_object(
                Bucket=destination_bucket,
                CopySource={'Bucket': source_bucket, 'Key': key}, 
                Key=new_key
            )
            
            # Delete from upload bucket
            s3.delete_object(Bucket=source_bucket, Key=key)
            
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File organized successfully'})
        }
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to organize file: {str(e)}'})
        }
