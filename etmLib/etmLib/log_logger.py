import logging
import os
import sys
import boto3
from inspect import currentframe

def log_init(nameV, log_level):
    
    """
    Function defines the log file name and output path, as well as the
    logging level.
    log_p = print statement 
    log_d = debug statement 
    """
   
    global logger
    logger = logging.getLogger(nameV)
    FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT,level=logging.INFO,datefmt='%H:%M:%S')
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.setLevel(log_level)

    # NEXT add a log file
    log_path = os.path.join('.', 'log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_name = nameV + '.log'
    log_file = os.path.join(log_path, log_name)

    fh = logging.FileHandler(log_file, mode='w')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMAT, datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    
# print statement - needs to be an f string
# screen and log file
def log_p(my_mesg):
    logger.info(my_mesg)

# debug statement - needs to be an f string
# screen only
def log_d(my_mesg) -> object:
    logger.debug(my_mesg)
    

def log_get_line_number():
    cf = currentframe()
    return cf.f_back.f_lineno


def s3_save_log_file(s3_output_path):

        s3 = boto3.client('s3')
        log_files = os.listdir("./log")
        for lf in log_files:
            if '.log' in lf:
                local_file = './log/' + lf
                with open(local_file, "rb") as f:
                    bucket = s3_output_path.split('/')[0]
                    prefix = '/'.join(s3_output_path.split('/')[1:])
                    bucket_filepath = prefix + '/log/' + lf
                    print(bucket, bucket_filepath)
                    s3.upload_fileobj(f, bucket, bucket_filepath)
                f.close()

