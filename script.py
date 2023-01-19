import boto3
import sys

def createNewUser(user_name, iam, managed_user_policies, list_of_groups_names, iam_resource):
    try:
        new_user_name = "new-{}".format(user_name)
        iam.create_user(UserName=new_user_name)
        
        for policies in managed_user_policies['AttachedPolicies']:
            iam.attach_user_policy(UserName=new_user_name, PolicyArn=policies['PolicyArn'])
        
        for group_name in list_of_groups_names:
            iam.add_user_to_group(GroupName=group_name, UserName=new_user_name)
        
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

def searchUser(env, iam, paginator, access_key, list_args, iam_resource):
    print('\nSearching for KEY on {} account...'.format(env))
    for user in iam.list_users()['Users']:
        user_name = user['UserName']
        for response in paginator.paginate(UserName=user_name):
            if len(response['AccessKeyMetadata']) > 0:
                access_key_metadata = response['AccessKeyMetadata'][0]
                if access_key == access_key_metadata['AccessKeyId'] or access_key in access_key_metadata['AccessKeyId']:
                    inline_user_policies = iam.list_user_policies(UserName=user_name)
                    managed_user_policies = iam.list_attached_user_policies(UserName=user_name)
                    raw_list_of_groups = iam.list_groups_for_user(UserName=user_name)
                    list_of_groups_names = [group['GroupName'] for group in raw_list_of_groups['Groups']]
                    print(' ')
                    print('=' * 50)
                    print('Key found!\n \n{} in {} user. \nSSO: {}'.format(access_key_metadata['AccessKeyId'], user_name, env))
                    print('\nManaged Policies: {}'.format(managed_user_policies))
                    print('\nInline Policies: {}'.format(inline_user_policies))
                    print('\nGroups: {}'.format(list_of_groups_names))
                    print('=' * 50)

                    if len(list_args) == 3:
                        if list_args[1] == "create":
                            createNewUser(user_name, iam, managed_user_policies, list_of_groups_names, iam_resource)

def setupSession(list_args):
    if len(list_args) == 1:
        myfile = open('/home/ulisses/.aws/credentials', 'r')
        for line in myfile:
            if line[0] == '[' and line[len(line) - 2]  == ']':
                env = line[1:(len(line) - 2)]
                session = boto3.Session(profile_name=env)
                iam = session.client('iam')
                iam_resource = session.resource('iam')
                paginator = iam.get_paginator('list_access_keys')
                searchUser(env, iam, paginator, list_args[0], list_args, iam_resource)
        myfile.close()
    elif len(list_args) == 3:
        try:
            session = boto3.Session(profile_name=list_args[2])

            iam = session.client('iam')
            iam_resource = session.resource('iam')
            paginator = iam.get_paginator('list_access_keys')
            searchUser(list_args[2], iam, paginator, list_args[0], list_args, iam_resource)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    list_args = [arg for arg in sys.argv[1:]]
    if len(list_args) == 0:
        print("Provide, at least, an access key to search a user in aws accounts.")
    elif len(list_args) > 3:
        print("## Too many arguments, you only need to pass an access key.")
    else:
        setupSession(list_args)


#print("Deactivating Key for the following users: " + user_name)
#iam.update_access_key(UserName=user_name, AccessKeyId=access_key_metadata['AccessKeyId'], Status='Inactive')