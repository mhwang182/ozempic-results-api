import boto3
from botocore.config import Config
from flask import current_app
from werkzeug.local import LocalProxy


def upload_image_s3(image, filename):    
    try:
        print('trying upload')
        s3.upload_fileobj(
            image,
            str(bucketName),
            filename,
            ExtraArgs={'ContentType': image.content_type}
        )
    except Exception as e:
        print(str(e))
        return False
    return True


def get_presigned_url(imageId):
    id = imageId.split('>')[1]
    url = None
    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': str(bucketName),
                'Key': str(id)
            },
            ExpiresIn=3600
        )
    except Exception as e:
        print(str(e))

    return url


def get_s3():
    S3_access_key_id = current_app.config['S3_ACCESS_KEY_ID']
    S3_secret_access_key = current_app.config['S3_SECRET_ACCESS_KEY']
    S3_endpoint_url = current_app.config['S3_ENDPOINT_URL']

    my_config = Config(
        signature_version = 'v4',
    )
    s3 = boto3.client(
            "s3",
            aws_access_key_id=S3_access_key_id,
            aws_secret_access_key=S3_secret_access_key,
            endpoint_url=S3_endpoint_url,
            config=my_config
        )
    return s3

def get_bucket_name():
    return current_app.config['BUCKET_NAME']

bucketName = LocalProxy(get_bucket_name)
s3 = LocalProxy(get_s3)
