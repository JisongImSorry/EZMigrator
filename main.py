import inquirer

import aws
import util
import grfd
import os

print("_       __     __                                      ___________   __  ____                  __")
print("| |     / /__  / /________  ____ ___  ___              / ____/__  /  /  |/  (_)___ __________ _/ /_____  _____")
print("| | /| / / _ \/ / ___/ __ \/ __ `__ \/ _ \   ______   / __/    / /  / /|_/ / / __ `/ ___/ __ `/ __/ __ \/ ___/")
print("| |/ |/ /  __/ / /__/ /_/ / / / / / /  __/  /_____/  / /___   / /__/ /  / / / /_/ / /  / /_/ / /_/ /_/ / /")
print("|__/|__/\___/_/\___/\____/_/ /_/ /_/\___/           /_____/  /____/_/  /_/_/\__, /_/   \__,_/\__/\____/_/")
print("                                                                           /____/")
print("Developed By - JiSong")

print("This CLI tool will guide you on migrating from AWS S3 to BNB Greenfield in a SIMPLE WAY :) ")
print("")
print("")

os.makedirs("./tmp", exist_ok=True)

# STEP 1. AWS Configuration
# Get AWS Credentials
s3Client, s3Resource = aws.get_aws_credentials()

# Check if GNFD Credentials exist
print("Checking if GNFD Credentials exist...")
print("")
print("")
grfd.check_grfd_credential()

# Get List of my AWS Buckets
myBuckets = aws.list_buckets(s3Resource)

print("I've found these buckets in your AWS account!")
print("")
print("")

questions = [
  inquirer.List('targetBucket',
                message="Which bucket whould you like to migrate?",
                choices=myBuckets,
            ),
]

answers = inquirer.prompt(questions)
targetBucket = answers['targetBucket']
targetAwsBucket = targetBucket[:]

print("You've selected " + targetBucket + " as your target bucket!")
print("")

print("AWS Configuration complete!")
print("")

# STEP 2. BNB Greenfield Configuration
print("Starting BNB Greenfield Configuration...")
print("")

# Get Primary SP
serviceProviders, serviceProvidersId = grfd.get_service_providers()

questions = [
  inquirer.List('primarySP',
                message="Do you have any preference on BNB Greenfield Service Provider?",
                choices=["No", "Yes, Let me choose one"],
            ),
]
answers = inquirer.prompt(questions)

primarySP=serviceProvidersId[0]
primarySPName=serviceProviders[0]
if(answers['primarySP'] == "Yes, Let me choose one"):
    questions = [
        inquirer.List('primarySP',
                    message="Which BNB Greenfield Service Provider would you like to use?",
                    choices=serviceProviders,
                ),
    ]
    answers = inquirer.prompt(questions)
    primarySP = serviceProvidersId[serviceProviders.index(answers['primarySP'])]
    primarySPName = answers['primarySP']

print("Using [ " + primarySPName + " ] as your primary service provider :)")
print("")

targetBucketName =  targetBucket + "-" + util.rand_string().lower()
targetBucketLocation = "gnfd://" + targetBucketName 

print("How about using bucket name : " + targetBucketName + " :)")

questions = [
  inquirer.List('bucketName',
                message="Do you have any preference on the name of the bucket?",
                choices=["No, I'll go with your pick", "Yes, I have a better name"],
            ),
]
answers = inquirer.prompt(questions)

if(answers['bucketName'] == "Yes, I have a better name"):
    questions = [
        inquirer.Text('bucketName',
                    message="What is your preferred bucket name?",
                ),
    ]
    answers = inquirer.prompt(questions)
    targetBucketName = answers['bucketName']
    targetBucketLocation = "gnfd://" + targetBucketName

while True:
    # Create Bucket
    bucketCreationRes = grfd.create_grfd_bucket(targetBucketLocation, primarySP, primarySPName)
    if(bucketCreationRes == 0):
        break
    else:
        questions = [
        inquirer.Text('bucketName',
                    message="What is your preferred bucket name?",
                ),
        ]
        answers = inquirer.prompt(questions)
        targetBucketName = answers['bucketName']
        targetBucketLocation = "gnfd://" + targetBucketName

print("Migrating files...")
files2Migrate = aws.list_files(s3Resource, targetBucket)
print(files2Migrate)

for file in files2Migrate:
    fileName=file[:]
    if fileName.endswith("/"):
        continue
    aws.download_file(s3Client, targetBucket, fileName)
    content_type = aws.get_file_content_type(s3Client, targetAwsBucket, fileName)
    uploadRes = grfd.upload_file(targetBucketName, fileName, content_type)
    if(uploadRes == -1):
        print("Error uploading file : " + fileName)
        print("Canceling creation...")
        grfd.cancel_create_object(targetBucketName, fileName)
        print("Retrying,..")
        uploadRes = grfd.upload_file(targetBucketName, fileName, content_type)
    print("")

print("Migration complete!")