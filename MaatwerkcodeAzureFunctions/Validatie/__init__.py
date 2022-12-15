import logging
from urllib.request import url2pathname

import azure.functions as func
from azure.storage.blob import BlobServiceClient

import os

import json
import cjvalpy

import urllib
from pathlib import Path

from lxml import etree

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    storageConnString= os.environ['AzureStorageConnectionString']
    # funcToken = os.environ['validationFunctionToken'] #TODO: Not implemented

    filename=req.headers.get("filename")
    filepath = req.headers.get("filepath")
    filepath = filepath.replace('testing-portaal/','')
    if filename is None:
        return func.HttpResponse('User input error, missing filename header', status_code=400)
    if filepath is None:
        return func.HttpResponse('User input error, missing filepath header', status_code=400)
    
    #Retrieving blob
    container_name='testing-portaal'
    blobService = BlobServiceClient.from_connection_string(conn_str=storageConnString)
    blobCli= blobService.get_blob_client(container_name, filepath )
    responseBody = blobCli.download_blob().readall()

    if filename.endswith('json'):
        try:
            valid = validateCityJSON(responseBody)
        except Exception as inst:
            logging.error(inst)
            return (func.HttpResponse("Issue with CityJSON validation: validation library not working properly with this file.", status_code=500))

    elif filename.endswith('gml'):
        try:
            valid = validateCityGML(responseBody)
        except Exception as inst:
            logging.error(inst)
            return (func.HttpResponse("Issue with CityGML validation: validation library not working properly with this file.", status_code=500))

    headers={'valid':str(valid)}

    return (func.HttpResponse(f"Provided file is valid: {valid}", status_code=200, headers=headers))

def validateCityJSON(responseBody):
    """
    Validates a response body (cityJSON), according to cityJSON specifications

    Args:
        responseBody: API call response body, cityJSON encoding expected.
    
    Returns:
        Boolean on whether the data is valid
    """
    info = responseBody.decode('utf-8')
    val = cjvalpy.CJValidator([info])
    re = val.validate()
    logging.info("Successfully validated")
    # logging.info(val.get_report()) #TODO: check library versions: this goes wrong

    if re:
        return True
    return False

def validateCityGML(responseBody):
    """
    Validates a response body (cityGML), according to cityGML specifications. Only suitable for 
    trusted data (vulnerable for billion laughs and quadratic blowup attacks)

    Args:
        responseBody: API call response body, cityJSON encoding expected.
    
    Returns:
        Boolean on whether the data is valid
    """
    url = "https://schemas.opengis.net/citygml/profiles/base/2.0/CityGML.xsd" 
    xsd_root  = etree.fromstring(urllib.request.urlopen(url).read())
    xml_root = etree.fromstring(responseBody)
    	
    schema = etree.XMLSchema(xsd_root)
    parser = etree.XMLParser(schema = schema)

    try:
        schema.assert_(xml_root)
        return True
    except etree.XMLSyntaxError as e:
        logging.info(f"Invalid document\n================\nError {e}")
        log = schema.error_log
        logging.info(log)
    except AssertionError as e:
        logging.info( f"Invalid document\n================\nError {e}")
    return False