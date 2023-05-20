import boto3
import inquirer

def is_aws_credentials_valid(s3Client):
    try:
        s3Client.list_buckets()
        return True
    except:
        return False

def get_aws_credentials():
  questions = [
    inquirer.Text('aws_access_key_id', message="Please provide your AWS Access Key ID"),
    inquirer.Text('aws_secret_access_key', message="Please provide your SECRET AWS Access Key ID"),
  ]

  answers = inquirer.prompt(questions)

  s3Client = boto3.client(
      's3',
      aws_access_key_id=answers['aws_access_key_id'],
      aws_secret_access_key=answers['aws_secret_access_key'],
  )
  s3Resource = boto3.resource(
      's3',
      aws_access_key_id=answers['aws_access_key_id'],
      aws_secret_access_key=answers['aws_secret_access_key'],
  )

  if not is_aws_credentials_valid(s3Client):
      print("Invalid AWS Credentials. Please try again.")

  return s3Client, s3Resource

def list_buckets(s3Resource):
  buckets = []
  s3 = s3Resource
  for bucket in s3.buckets.all():
      buckets.append(bucket.name)
  return buckets

def list_files(s3Resource, bucket):
  files = []
  s3 = s3Resource
  my_bucket = s3.Bucket(bucket)

  for file in my_bucket.objects.all():
      files.append(file.key)
  return files

def download_file(s3Client, bucket, object):
  print("Downloading file " + object + " from " + bucket)
  s3 = s3Client
  s3.download_file(bucket, object, 'tmp/' + object)
  print("Download " + object + " from " + bucket + " complete!")

def get_file_content_type(s3Client, bucket, key):
  s3 = s3Client
  response = s3.head_object(
      Bucket=bucket,
      Key=key
  )
  return response["ResponseMetadata"]["HTTPHeaders"]["content-type"]
