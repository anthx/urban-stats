import os, datetime, requests
import boto3
import botocore


def check_file_is_young(filename: str) -> bool:
    """
    Returns true if filename is < 1 month old, false otherwise or not exist
    :param filename: str of the filename
    :return: bool
    """
    try:
        s3_connection = boto3.resource('s3')
        path_age = s3_connection.Object('urban-statistics', filename).last_modified.timestamp()
        month_ago = datetime.datetime.now() - datetime.timedelta(days=30)

        if path_age > month_ago.timestamp():
            return True
        else:
            return False
    except botocore.exceptions.ClientError:
        return False
