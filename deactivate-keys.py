import boto3
import json
import sys

def searchUser(env, iam, paginator, access_key):
    print('\nSearching for KEY on {} account...'.format(env))
    for user in iam.list_users()['Users']:
        user_name = user['UserName']
        for response in paginator.paginate(UserName=user_name):
            if len(response['AccessKeyMetadata']) > 0:
                access_key_metadata = response['AccessKeyMetadata'][0]
                if access_key == access_key_metadata['AccessKeyId'] or access_key in access_key_metadata['AccessKeyId']:
                    print(' ')
                    print('Key found!\n{} \nUser: {} \nSSO: {}'.format(access_key_metadata['AccessKeyId'], user_name, env))
                    iam.update_access_key(UserName=user_name, AccessKeyId=access_key_metadata['AccessKeyId'], Status='Inactive')
                    return 1


def setupSession(list_args):
    myfile = open('/home/ulisses/.aws/credentials', 'r')
    search_status = 0
    for line in myfile:
        if line[0] == '[' and line[len(line) - 2]  == ']':
            env = line[1:(len(line) - 2)]
            session = boto3.Session(profile_name=env)
            iam = session.client('iam')
            paginator = iam.get_paginator('list_access_keys')
            search_status = searchUser(env, iam, paginator, list_args[0])
        if search_status:
            break
    myfile.close()

if __name__ == "__main__":
    try:
        list_args = [arg for arg in sys.argv[1:]]
        setupSession(list_args)
    except:
        print("")