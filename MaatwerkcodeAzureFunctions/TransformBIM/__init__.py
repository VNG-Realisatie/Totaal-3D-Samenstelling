import logging
import os
import io

import azure.functions as func
from azure.storage.blob import BlobServiceClient

import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    """ 
    Moves data from a spe
    """
    logging.info('Python HTTP trigger function processed a request.')


    baseurl = r"https://bim.clearly.app/api/"
    organisationId = "61924d981cedc370173c7d5a"
    projectId = "62aee7a413866868a5a18efe" # project voor alle transformaties op clearly

    storageConnString= os.environ['AzureStorageConnectionString']
    bimAuthToken = os.environ['clearlyAuthorizationToken']
    funcToken = os.environ['transformBimFunctionToken']


    if (req.params.get('Method')=="OPTIONS") or req.headers.get('Method')=="OPTIONS" or req.method=="OPTIONS":
         return func.HttpResponse(
            headers={"access-control-allow-methods":"OPTIONS, POST",
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


    logging.info('Pinging the API')
    url = baseurl + "ping"
    response = requests.request("GET", url)
    if response.status_code!=200:
        return func.HttpResponse('Ping not alive', status_code=503)
      
    logging.info("Checking if building (model) name already exists")
    # getting all projects
    url = baseurl + f"organisations/{organisationId}/projects/{projectId}/models"
    headers = {'Authorization': f'Bearer {bimAuthToken}'}
    response = requests.request("GET", url, headers=headers)
    json_data = response.json()

    #matching projects
    modelId = None
    filenameStripped = filename.replace('.ifc','')
    if json_data!=[]: #checking if there are any models
        for model in json_data:
            if model['name']==filenameStripped:
                modelId = model["_id"]

    if modelId == None:
        logging.info("Creating new model")
        payload=f'name={filenameStripped}'
        headers= {
            'Authorization': f'Bearer {bimAuthToken}',
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code!=200:
            return func.HttpResponse('Could not create a new model', status_code=500)
        modelId = response.json()["_id"] 
        logging.info(f"Created model {filenameStripped}")

    #File processing starts here
    logging.info('Retrieving blob')
    container_name='testing-portaal'
    blobService = BlobServiceClient.from_connection_string(conn_str=storageConnString)
    blobCli= blobService.get_blob_client(container_name, filepath )
    responseBody = blobCli.download_blob().readall()
    if len(responseBody)==0:
        return func.HttpResponse('Issue with blob data, missing a body', status_code=400)
    bytes_out = io.BytesIO()
    bytes_out.write(responseBody)


    logging.info("Uploading data")
    url= baseurl + f"organisations/{organisationId}/projects/{projectId}/models/{modelId}/versions?organisationId={organisationId}&projectId={projectId}&modelId={modelId}"
    multipart_form_data={'version': ('20220530_22018_Kwekerijweg Den Haag.ifc', responseBody)}
    headers= {
            'Authorization': f'Bearer {bimAuthToken}',
            'cityjson':'true'
            }
    response = requests.request("POST", url, headers=headers, files=multipart_form_data)
    modelVersion=response.json()['version']

    headers = {
        'projectId':projectId,
        'modelId':modelId,
        'version':str(modelVersion)
    }
    logging.info("Data successfully uploaded")
    return func.HttpResponse(f"Data successfully uploaded to BIM server, ['projectId':{projectId},'modelId':{modelId},'version':{modelVersion}]", status_code=200, headers=headers) 