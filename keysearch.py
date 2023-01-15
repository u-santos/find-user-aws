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
                        
                        print("\nKey found!\n \n{} in {} user. \nSSO: {}".format(KEY, user_name, env))
                        print("\nInline Policies:\n{}".format(inline_user_policies))
                        print("\nManaged Policies:\n{}".format(managed_user_policies))
                        print(" ")

                        try:
                            new_user_name = "TEST-{}".format(user_name)
                            iam.create_user(UserName=new_user_name)
                            for policies in managed_user_policies['AttachedPolicies']:
                                iam.attach_user_policy(UserName=new_user_name, PolicyArn=policies['PolicyArn'])
                            access_key_pair = user.create_access_key_pair()
                            print("\nUser Created!")
                            for response in paginator.paginate(UserName=new_user_name):
                                print(response)
                        except Exception as e:
                            print("Failed: Error on create a new user, please contact your administrator.")
                            print(e)
    if search:
        break
myfile.close()

if not search:
    print("User not found!")
