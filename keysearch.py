import boto3
import sys

myfile = open("/home/ulisses/.aws/credentials", "r")
KEY = sys.argv[1]
search = False
for line in myfile:
    if line[0] == "[" and line[len(line) - 2]  == "]":
        env = line[1:(len(line) - 2)]
        session = boto3.Session(profile_name=env)

        iam = session.client('iam')
        paginator = iam.get_paginator('list_access_keys')

        print("\nSearching for KEY on SSO: {} account...".format(env))
        for user in iam.list_users()['Users']:
            user_name = user['UserName']
            for response in paginator.paginate(UserName=user_name):
                if len(response['AccessKeyMetadata']) > 0:
                    access_key_metadata = response['AccessKeyMetadata'][0]
                    if KEY == access_key_metadata['AccessKeyId']:
                        search = True
                        inline_user_policies = iam.list_user_policies(UserName=user_name)
                        managed_user_policies = iam.list_attached_user_policies(UserName=user_name)
                        
                        print("\nKey found!\n \n{} in {} user. \nSSO: {}".format(sys.argv[1], access_key_metadata['UserName'], env))
                        print("\nInline Policies: {}".format(inline_user_policies))
                        print("\nManaged Policies: {}".format(managed_user_policies))
    if search:
        break
myfile.close()

if not search:
    print("User not found!")
