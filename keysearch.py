import boto3
import sys

def createNewUser(user_name, iam, managed_user_policies, iam_resource):
    try:
        new_user_name = "new-{}".format(user_name)
        iam.create_user(UserName=new_user_name)
        for policies in managed_user_policies['AttachedPolicies']:
            iam.attach_user_policy(UserName=new_user_name, PolicyArn=policies['PolicyArn'])
        new_user_key = iam_resource.User(new_user_name)
        access_key_pair = new_user_key.create_access_key_pair()
        
        print(' ')
        print('=' * 50)
        print('USER CREATED')
        print('NEW KEY GENERATED - PLEASE RECORD THE NEW KEYS')
        print('THEY WILL NOT BE DISPLAYED AGAIN')
        print('=' * 50)
        print('\nid:', access_key_pair.access_key_id)
        print('secret:', access_key_pair.secret)
        print('status:', access_key_pair.status)
    except Exception as e:
        print("Failed: Error to create new user.")
        print(e)

def searchKey(access_key):
    search = False
    myfile = open('/home/ulisses/.aws/credentials', 'r')

    for line in myfile:
        if line[0] == '[' and line[len(line) - 2]  == ']':
            env = line[1:(len(line) - 2)]
            session = boto3.Session(profile_name=env)

            iam = session.client('iam')
            iam_resource = session.resource('iam')
            paginator = iam.get_paginator('list_access_keys')

            print('\nSearching for KEY on {} account...'.format(env))
            for user in iam.list_users()['Users']:
                user_name = user['UserName']
                for response in paginator.paginate(UserName=user_name):
                    if len(response['AccessKeyMetadata']) > 0:
                        access_key_metadata = response['AccessKeyMetadata'][0]
                        if access_key == access_key_metadata['AccessKeyId']:
                            search = True
                            inline_user_policies = iam.list_user_policies(UserName=user_name)
                            managed_user_policies = iam.list_attached_user_policies(UserName=user_name)
                            
                            print('\nKey found!\n \n{} in {} user. \nSSO: {}'.format(access_key, user_name, env))

                            createNewUser(user_name, iam, managed_user_policies, iam_resource)
        if search:
            break
    myfile.close()

    if not search:
        print('\nUSER NOT FOUN')

if __name__ == "__main__":
    searchKey(sys.argv[1])