import json
import os
import boto3
from botocore.exceptions import ClientError

def get_secret(dbsecret_name_env='DBSECRET_NAME'):
    """Retrieve database credentials from Secrets Manager

    :param str dbsecret_name_env: Name of the environment variable from which to retrieve the secret name
    """
    secret_name = os.environ[dbsecret_name_env]
    region_name = os.environ['AWS_REGION']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        print("Getting secret value...")
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        raise e

    secret = get_secret_value_response['SecretString']
    print("Secret retrieved successfully!")

    return json.loads(secret)

def get_db_config(dbname_env='DBNAME'):
    """Retrieve database credentials from Secrets Manager

    :param str dbname_env: Name of the environment variable from which to retrieve the database name
    """
    secret_dict = get_secret()
    dbname = os.environ['DBNAME']
    dbconfig = {
        "host": secret_dict["host"],
        "user": secret_dict["username"],
        "password": secret_dict["password"],
        "dbname": dbname,
        "port": secret_dict["port"]
    }
    return dbconfig

def get_proxy_parameters(event):
    """Retrieve proxy parameters from API Gateway event"""
    path_parameters = event.get('pathParameters', {})
    proxy = path_parameters.get('proxy', None)
    if proxy is not None:
        proxy_parameters = proxy.split('/')
        return proxy_parameters
    else:
        return []