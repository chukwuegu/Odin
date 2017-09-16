import six
import environ

env = environ.Env()

AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION = env('DJANGO_AWS_S3_REGION')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')

AWS_S3_HOST = env('DJANGO_AWS_S3_HOST', default='s3-%s.amazonaws.com' % AWS_S3_REGION)
AWS_S3_SIGNATURE_VERSION = env('DJANGO_AWS_S3_SIGNATURE_VERSION', default='s3v4')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True

AWS_EXPIRY = 60 * 60 * 24 * 7

AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}
