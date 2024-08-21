import boto3
import urllib.parse
import os

from image_supporter import ImageFormatter


class S3ImageCompactSupporter:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.image_threshold = 1000000  # 1MB
        self.image_quality = 80
        self.default_image_type = 'jpeg'
        self.image_format_supporter = ImageFormatter(self.default_image_type)

        self.image_acl = 'public-read'

    def process_s3_metadata(self, event_records):
        for meta_data in event_records:
            s3_metadata = meta_data['s3']
            self._process_image(s3_metadata)

    def _process_image(self, s3_meta_data: dict):
        bucket_name = s3_meta_data['bucket']['name']
        key = urllib.parse.unquote_plus(s3_meta_data['object']['key'], encoding='utf-8')
        size = int(s3_meta_data['object']['size'])

        if size > self.image_threshold:
            image_path = self._image_download(bucket_name, key)
            transformed_image_path = self.image_format_supporter.compact_image(image_path, self.image_quality)
            self._upload_image(bucket_name, key, transformed_image_path)

    def _image_download(self, bucket_name, key):
        print('Downloading image from s3')
        image_download_path = '/tmp/' + key.split('/')[-1]
        self.s3_client.download_file(bucket_name, key, image_download_path)

        transformed_image_path = self.image_format_supporter.transform_image(image_download_path)

        print('Image downloaded to ' + transformed_image_path)
        return transformed_image_path

    def _upload_image(self, bucket_name, key, image_path):
        content_type = 'image/' + self.default_image_type

        self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=open(image_path, 'rb'), ContentType=content_type)
        os.remove(image_path)
