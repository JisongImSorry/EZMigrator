import subprocess
import inquirer
import os
import re

def upload_file(bucket, object, contentType):
    bucket = "gnfd://" + bucket
    object_location = "tmp/" + object
    print("Uploading file " + object + " to " + bucket)
    print(bucket + "/" + object)
    result = subprocess.call(["./gnfd-cmd", "storage", "put", "--contentType", contentType, object_location, bucket + "/" + object])
    print("Upload " + object + " to " + bucket + " complete!")

def create_grfd_bucket(bucket, primarySP):
    print("Creating bucket", bucket, "in BNB Greenfield...")
    print("using primary SP", primarySP)
    createBucketRes = subprocess.check_output(["./gnfd-cmd", "storage", "make-bucket", "--primarySP", primarySP+"", bucket])
    if "error" in createBucketRes.decode():
        print(createBucketRes.decode())
        print("Error creating bucket. Please try again with another name.")
        return -1
    else:
        print("Bucket created!")
        return 0
    
def get_service_providers():
    print("Getting service providers...")

    serviceProviders = subprocess.check_output(["./gnfd-cmd", "ls-sp"])
    serviceProviderString=serviceProviders.decode()
    serviceProviders = re.findall(r'endpoint:(.*?),', serviceProviderString)
    serviceProvidersId = re.findall(r'operator-address:(.*?),', serviceProviderString)

    return serviceProviders, serviceProvidersId

def check_grfd_credential():
    file_path = './key.json'  

    if os.path.exists(file_path):
        # Credentials exist
        print("Credentials exist!")
    else:
        # Credentials do not exist. Make a new one
        print("Credentials do not exist!")
        print("Making new credentials to access to GNFD...")
        
        questions = [
        inquirer.Text('privKey', message="Please provide your BNB Greenfield Private Key"),
        ]
        answers = inquirer.prompt(questions)
        userPrivKey = answers['privKey']

        with open('key.txt', 'w') as f:
            f.write(userPrivKey)

        result = subprocess.call(["./gnfd-cmd", "gen-key", "-privKeyFile", "key.txt", "key.json"])
        print("Credentials created!")