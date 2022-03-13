import os

import pandas as pd
import requests
import json
import sys
import boto3
from botocore.exceptions import ClientError


# aws stuff here

##-----------------------------------------------------------------------------------------------------------
#       S3 AWS UTILITY FUNCIONS

#           def s3_bucket_analyze(bucket, prefix):
#           def s3_bucket_prefixes(bucket_p, performer, prefix_with_slash):

##-----------------------------------------------------------------------------------------------------------

def _get_bucket(s3_full_path):
    bucket = s3_full_path.split('/')[2]
    pre_path = '/'.join(s3_full_path.split('/')[3:])
    return (bucket, pre_path)

def s3_upload_chs(local_file_name, full_s3_url, delete_local=True):

    _save_chs_global_keys
    REGION_NAME='us-west-2'

    print (local_file_name, full_s3_url, delete_local)

    (bucket, bucket_filepath) = _get_bucket(full_s3_url)
    
    s3 = boto3.client('s3', 
                      aws_access_key_id=chs_AccessKeyId, 
                      aws_secret_access_key=chs_SecretAccessKey, 
                      aws_session_token=chs_Token,
                      region_name=REGION_NAME
                      )
    
    with open(local_file_name, "rb") as f:
        s3.upload_fileobj(f, bucket, bucket_filepath)
    if delete_local:
        os.remove(local_file_name)

def _s3_list_pseudo_subdirs(bucket, prefix_with_slash):

    subfolder_list = []
    #Make sure you provide / in the end

    a = prefix_with_slash.split('/')
    prefix_with_slash='/'.join(a[1:])
    prefix = prefix_with_slash

    print(f'prefix_with_slash, {prefix_with_slash}')

    #client = boto3.client('s3')
    session = boto3.Session(profile_name='smart')
    client = session.client('s3')

    try:
        result = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
        try:
            for o in result.get('CommonPrefixes'):
                #print ('sub folder : ', o.get('Prefix'))
                subfolder_list.append(o.get('Prefix'))
            return subfolder_list
        except:
            return ['emptyDir', 'Maybe']
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print('no such bucket', bucket)
            return ['NoSuchBucket', 'Really_No_such_bucket']
        else:
            print("Unexpected error: %s" % e)
            return ['Unexpected', 'Really_unexpected']

def s3_bucket_prefixes(bucket_p, performer, prefix_with_slash):

    bucket = f'{bucket_p}{performer}'
    folders = _s3_list_pseudo_subdirs(bucket, prefix_with_slash)
    return folders

# 


def s3_bucket_analyze(bucket, prefix):

    objs = []

    print("bucket", bucket)
    print("prefix", prefix)

    bucket_name = bucket
    prefix = prefix

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    cnt=0
    storage_class_h = {'STANDARD' : 0,
                   'GLACIER' : 0,
                   'INTELLIGENT_TIERING' : 0,
                  }
    sum_class_h = {'STANDARD' : 0,
                   'GLACIER' : 0,
                   'INTELLIGENT_TIERING' : 0,
                  }
    sum = 0
    for obj in bucket.objects.filter(Prefix=prefix):
        storage_class_h[obj.storage_class] = storage_class_h[obj.storage_class] + 1
        cnt = cnt + 1
        if not cnt%1000:
            print(bucket, "bucket object count = ", cnt, flush=True)
        sum = sum + obj.size
        sum_class_h[obj.storage_class] = sum_class_h[obj.storage_class] + obj.size
        my_obj = {
                'bucket_name':obj.bucket_name,
                'key':obj.key,
                'size':obj.size,
                'class':obj.storage_class
                }
        objs.append(my_obj)

    print ("COUNT=", cnt)
    for ky in storage_class_h.keys():
        print(ky, storage_class_h[ky])
        sum = sum_class_h[ky]
        print(ky, sum_class_h[ky])
        gig = sum/(1024*1024*1024)
        print (ky, "GBYTES=", gig)
        if ky == 'GLACIER': 
            cost=.007
        else: 
            cost=.023
        print (ky, "Cost/Month=", gig * cost)
        print ("----" * 25)
    print("END LOOP")
    my_key = 'STANDARD'
    ret_gbytes = sum_class_h[my_key]/(1024*1024*1024)
    if (ret_gbytes < 1):
        ret_gbytes = 1
    ret_costs = .023 * ret_gbytes
    print('G:', ret_gbytes, ret_costs)
    return objs
   
                                                   

##-------------------------------------------------------------------------------------------------------------------
#       Authentication Functions
#
#   def auth_init(smart=True, chs=True):
#   def auth_user_scope_chs():
#   def auth_user_scope_smart():
#
##-------------------------------------------------------------------------------------------------------------------

def _return_chs_session_keys():
    url_loop_local = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/lsds-developer-ec2'
    r = requests.get(url_loop_local)
    chs_auth = json.loads(r.text)
    return chs_auth


def _get_aws_credentials_carefully_from_file(cred_file_path):
    ''' return an env dict for docker use
            and for setting the env in notebooks
            not necessary pretty - but gets us authenticated to access the necessary buckets
    '''


    # read text file into pandas DataFrame
    df = pd.read_table(cred_file_path, delimiter="=").T
    secret_be_careful = df['aws_secret_access_key '].values[0].replace(' ', '')
    secret_key = df['aws_access_key_id '].values[0].replace(' ', '')

    access_key = 'aws_access_key_id'.upper()
    access_secret = 'aws_secret_access_key'.upper()


    docker_env_dict = {
        access_key:secret_key,
       access_secret:secret_be_careful
    }
    return docker_env_dict


def _set_aws_environment(docker_env_dict):
    for i in docker_env_dict:
        #print(i, docker_env_dict[i])
        os.environ[i]=docker_env_dict[i]


def _smart_environment_set(): 
    '''check if the aws environ var set - if NOT then set them!
            - always return True
    '''
    key="AWS_ACCESS_KEY_ID"

    if key in os.environ:
        print('SMART Global Environment set correctly YES!', os.environ['AWS_ACCESS_KEY_ID'][0])
        return True
    else:
        print("Key does not exist - setting them from credentials")
        aws_credentials_file='/home/ec2-user/.aws/credentials'
        aws_env_dict = _get_aws_credentials_carefully_from_file(aws_credentials_file)
        #print(aws_env_dict)
        _set_aws_environment(aws_env_dict)
        return True
    

def _save_smart_global_keys():
    global smart_AccessKeyId 
    global smart_SecretAccessKey
    global smart_Token

    if _smart_environment_set():
        smart_AccessKeyId = os.environ['AWS_ACCESS_KEY_ID']
        smart_SecretAccessKey = os.environ['AWS_SECRET_ACCESS_KEY']
        smart_Token = ''
    else:
        print('something wrong in key chain no smart key pair')
        

def _save_chs_global_keys():
    c_auth = _return_chs_session_keys()
    global chs_AccessKeyId 
    chs_AccessKeyId = c_auth['AccessKeyId']
    global chs_SecretAccessKey
    chs_SecretAccessKey = c_auth['SecretAccessKey']
    global chs_Token
    chs_Token = c_auth['Token']


def auth_init(smart=True, chs=True):
    if smart:
        _save_smart_global_keys()
    
    if chs:
        _save_chs_global_keys()
        

def auth_user_scope_chs():
    os.environ['AWS_ACCESS_KEY_ID'] = chs_AccessKeyId
    os.environ['AWS_SECRET_ACCESS_KEY'] = chs_SecretAccessKey
    os.environ['AWS_SESSION_TOKEN'] = chs_Token

    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
    os.environ['AWS_REQUEST_PAYER'] = 'requester'
    print('CHS', os.environ['AWS_ACCESS_KEY_ID'])



def auth_user_scope_smart():
    os.environ['AWS_ACCESS_KEY_ID'] = smart_AccessKeyId
    os.environ['AWS_SECRET_ACCESS_KEY'] = smart_SecretAccessKey
    os.environ['AWS_SESSION_TOKEN'] = smart_Token

    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
    os.environ['AWS_REQUEST_PAYER'] = 'requester'
    print('Smart', os.environ['AWS_ACCESS_KEY_ID'])



