import json
from s3_handler import S3ImageCompactSupporter


def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    try:
        meta_datas = json.loads(event['Records'][0]['body'])['Records']
        image_compact_supporter = S3ImageCompactSupporter()
        image_compact_supporter.process_s3_metadata(meta_datas)
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
