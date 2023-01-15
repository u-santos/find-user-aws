import boto3
import sys

myfile = open("/home/ulisses/.aws/credentials", "r")

search = False
for line in myfile:
    if line[0] == "[" and line[len(line) - 2]  == "]":
        env = line[1:(len(line) - 2)]
        session = boto3.Session(profile_name=env)
        iam = session.client('iam')
        paginator = iam.get_paginator('list_access_keys')

        print("============================================================")
        print("\nSearching for KEY on SSO: {} account...".format(env))
        for user in iam.list_users()['Users']:
            for response in paginator.paginate(UserName=user['UserName']):
                if len(response['AccessKeyMetadata']) > 0:
                    if sys.argv[1] == response['AccessKeyMetadata'][0]['AccessKeyId']:
                        search = True
                        print("Key found! \n{} in {} user. \nSSO: {}".format(sys.argv[1], response['AccessKeyMetadata'][0]['UserName'], env))
                
    if search:
        break
myfile.close()

if not search:
    print("User not found!")
