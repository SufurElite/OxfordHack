import os, io
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format
import re
import pandas as pd
import json

def loadImageText(fPath):
    gcs_source_uri = "gs://revaise.appspot.com/"+fPath
    storage_client = storage.Client()
    
    match = re.match(r'gs://([^/]+)/(.+)', gcs_source_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    print(match.group(1))
    print(match.group(2))
    bucket = storage_client.get_bucket(bucket_name)
    # List objects with the given prefix.
    from time import sleep
    sleep(1)
    blob_list = list(bucket.list_blobs(prefix=prefix))
    
    print('Output files:')
    for blob in blob_list:
        print(blob.name)
    
    blob = bucket.get_blob(fPath)
    print("Starting Client")
    client = vision.ImageAnnotatorClient()
    print("downloading picture")
    content = blob.download_as_bytes()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    
    txt = response.full_text_annotation.text
    print(txt)
    with open("tmp_data.txt","w+") as f:
        f.write(txt)
    return txt

def loadPdfText(fPath):
    gcs_source_uri = "gs://revaise.appspot.com/"+fPath
    print(gcs_source_uri)
    #gcs_source_uri = "gs://revaise.appspot.com/images/picture-ScienceVideo Game Deep RL0.8575049874802985"
    gcs_destination_uri = "gs://revaise.appspot.com/TextOutput/"
    gcs_destination = vision.GcsSource(uri=gcs_destination_uri)
    mime_type = "application/pdf"
    # mime_type = "image/png"
    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    print(gcs_source_uri)
    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
    print(input_config)
    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)
    print(output_config)
    import time
    time.sleep(1)
    async_request = vision.AsyncAnnotateFileRequest(features=[feature], input_config=input_config, output_config=output_config)

    operation = client.async_batch_annotate_files(requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=420)
    
    storage_client = storage.Client()
    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)
    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)
    
    txt = ""
    for output in blob_list:
        
        json_string = output.download_as_string()
        if json_string!=b'':
            response = json.loads(json_string)

            # The actual response for the first page of the input file.
            for j in response['responses']:
                txt+=j['fullTextAnnotation']['text']+" "
    with open("park.txt","w+") as f:
        f.write(txt)
    for blob in blob_list:
        blob.delete()
    print(txt)
    return txt

if __name__=="__main__":
    loadImageText()