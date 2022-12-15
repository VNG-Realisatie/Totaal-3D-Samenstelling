import logging
import os
import io

import azure.functions as func
from azure.storage.blob import BlobServiceClient

import boto3
from botocore.exceptions import ClientError


def main(req: func.HttpRequest) -> func.HttpResponse:
    """ 
    Allows user to move data from Azure Storage to AWS S3 bucket
    """
    logging.info('Python HTTP trigger function processed a request.')

    bucketName="t3d-share"
    awsAccessKeyId = os.environ['S3AccessKey']
    awsSecretKey =os.environ['S3SecretKey']
    storageConnString= os.environ['AzureStorageConnectionString']
    funcToken = os.environ['sendToBeheertoolFunctionToken']

    if (req.params.get('Method')=="OPTIONS") or req.headers.get('Method')=="OPTIONS" or req.method=="OPTIONS":
         return func.HttpResponse(
            headers={"access-control-allow-methods":"OPTIONS, PUT",
                    "access-control-allow-headers":"Content-Type"}
        )

    logging.info('Checking the token')
    authToken = req.headers.get("Authorization")
    isTokenValid = ((authToken==funcToken) or (authToken==f"Bearer {funcToken}")) # static token

    if not isTokenValid:
        return func.HttpResponse('Invalid token', status_code=401)
    logging.info("Authentication succeeded")

    #Checking headers
    filename=req.headers.get("filename")
    filepath = req.headers.get("filepath")
    filepath = filepath.replace('testing-portaal/','')
    if filename is None:
        return func.HttpResponse('User input error, missing filename header', status_code=400)
    if filepath is None:
        return func.HttpResponse('User input error, missing filepath header', status_code=400)
    
    #Retrieving blob
    if not (('.json' in filename) or ('.gml' in filename)):
        return func.HttpResponse('User input error, data provided is not a json or gml', status_code=400)
    obj_id = filename.replace('.json','')
    obj_id = obj_id.replace('.gml','')

    # For rioned data
    if obj_id.startswith('DenHaag') or obj_id.startswith('Rotterdam'):
        s3location = f'happyflow-sewer-update/{filename}'
    else:
        s3location = f'happyflow-updates/new/NL.IMBAG.Pand.{filename}'
        if len(obj_id)!=16:
            return (func.HttpResponse('User input error: objectId should be 16 characters long', status_code=400))
        if not obj_id.isdecimal():
            return (func.HttpResponse('User input error: objectId should only contain numbers', status_code=400))


    container_name='testing-portaal'
    blobService = BlobServiceClient.from_connection_string(conn_str=storageConnString)
    blobCli= blobService.get_blob_client(container_name, filepath )
    responseBody = blobCli.download_blob().readall()

    if len(responseBody)==0:
        return func.HttpResponse('Issue with blob data, missing a body', status_code=400)
    bytes_out = io.BytesIO()
    bytes_out.write(responseBody)
    bytes_out.seek(0)
    
    s3_client = boto3.client(
            's3',
            aws_access_key_id=awsAccessKeyId,
            aws_secret_access_key=awsSecretKey,
    )

    try:
        # obj.upload_fileobj(bytes_out)
        
        response = s3_client.put_object(Body=bytes_out, Bucket=bucketName, Key=s3location)
        return (func.HttpResponse('Successful upload', status_code=200))
    except ClientError as e:
        logging.error(e)
        return func.HttpResponse('Error with S3 upload', status_code=400)
