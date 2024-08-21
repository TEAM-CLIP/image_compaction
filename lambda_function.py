import os
import sys
import boto3
import urllib.parse
from PIL import Image
import json

s3_client = boto3.client('s3')

image_threshold = 1000000  # 1MB
image_quality = 80


def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    try:
        s3_details = json.loads(event['Records'][0]['body'])['Records']
        for s3_detail in s3_details:
            print(s3_detail)
            process_image(s3_detail)
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Error processing image'
        }

    return {
        'statusCode': 200,
        'body': 'Image processed successfully'
    }


def process_image(s3_detail: dict):
    image_detail = s3_detail['s3']
    bucket_name = image_detail['bucket']['name']
    key = urllib.parse.unquote_plus(image_detail['object']['key'], encoding='utf-8')
    size = int(image_detail['object']['size'])

    if size > image_threshold:
        compact_image(bucket_name, key)


def image_download(bucket_name, key):
    print('Downloading image from s3')
    image_download_path = '/tmp/' + key.split('/')[-1]
    s3_client.download_file(bucket_name, key, image_download_path)

    print('Image downloaded to ' + image_download_path)
    return image_download_path


def upload_image(bucket_name, key, image_path):
    content_type = 'image/'+key.split('.')[-1]
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=open(image_path, 'rb'), ContentType=content_type)
    os.remove(image_path)


def compact_image(bucket_name, key):
    image_path = image_download(bucket_name, key)
    with Image.open(image_path) as img:
        img.save(image_path, quality=image_quality)
        upload_image(bucket_name, key, image_path)
    return image_path
