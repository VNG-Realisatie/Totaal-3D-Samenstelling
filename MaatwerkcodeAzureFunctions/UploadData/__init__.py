import logging
import os

import json

import azure.functions as func
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest, outputBlob:func.Out[bytes]) -> func.HttpResponse:
    """ 
    Allows user to upload CityJSON files to Azure storage account for the T3D project, assigns random uid to the filename
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    storageConnString= os.environ['AzureStorageConnectionString']
    funcToken = os.environ['uploadFunctionToken']


    if (req.params.get('Method')=="OPTIONS") or req.headers.get('Method')=="OPTIONS" or req.method=="OPTIONS":
         return func.HttpResponse(
            headers={"access-control-allow-methods":"POST, OPTIONS, PUT",
                    "access-control-allow-headers":"Content-Type"}
        )


    logging.info('Checking the token')
    authToken = req.headers.get("Authorization")
    
    isTokenValid = ((authToken==funcToken) or (authToken==f"Bearer {funcToken}")) # static token

    if not isTokenValid:
        return func.HttpResponse('Invalid token', status_code=401)
    logging.info("Authentication succeeded")

    logging.info("Checking headers and header content")
    #TODO: move to a function/lib
    if "objectId" not in req.headers.keys():
        return (func.HttpResponse('User input error: objectId is a required header', status_code=400))
    objectId = req.headers.get("objectId")
    if len(objectId)!=16:
        return (func.HttpResponse('User input error: objectId should be 16 characters long', status_code=400))
    if not objectId.isdecimal():
        return (func.HttpResponse('User input error: objectId should only contain numbers', status_code=400))

    if "initiatorPersoon" in req.headers.keys():
        initiatorPersoon=req.headers.get("initiatorPersoon")
    else:
        initiatorPersoon="Unknown"

    if "initiatieSysteemVersie" in req.headers.keys():
        initiatieSysteemVersie =req.headers.get("initiatieSysteemVersie")
    else:
        initiatieSysteemVersie ="Unknown"
    

    logging.info('Extension check')
    try:
        body = json.loads(req.get_body().decode('utf-8'))
    except:
        return (func.HttpResponse('Invalid input file, accepts only CityJSON', status_code=400))


    if body['type']=="CityJSON":
        #Getting to the data
        data = req.get_body()
        req.headers.get("")
        filepath = f"in/amsterdam/{objectId}.json"

        metadata={
            "initiatorPersoon":initiatorPersoon,
            "initiatieSysteemObjectid":objectId,
            "naamBestand":f"{objectId}.json",
            "inputBestandsnaamLink":filepath,
            "initiatieSysteemId":"2", #Amsterdam
            "initiatieSysteemVersie": initiatieSysteemVersie 
        }
        
        logging.info('Uploading blob')
        container_name='testing-portaal'
        blobService = BlobServiceClient.from_connection_string(conn_str=storageConnString)
        blobCli= blobService.get_blob_client(container_name, filepath)
        
        blobCli.upload_blob(data=data,overwrite=True)
        blobCli.set_blob_metadata(metadata=metadata)
        
        # OLD method to upload data
        # outputBlob.set(data)
        
        return (func.HttpResponse('Successful upload', status_code=200, headers=metadata))
    else:
        return (func.HttpResponse('Invalid input file, accepts only CityJSON', status_code=400))
