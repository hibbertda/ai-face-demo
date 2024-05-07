# Azure AI Face API Demo

## Overview

This example demo application showcases the capabilities of the [Azure AI Face API]((https://learn.microsoft.com/en-us/python/api/overview/azure/cognitiveservices/face-readme?view=azure-python)), a powerful tool for image processing and analysis. By utilizing this API, developers can leverage advanced computer vision algorithms to modify images based on the position and measurements of the subject's face.

### Capabilities

- Detect and analyze facial features, including eyes, nose, mouth, and jawline
- Identify key facial attributes such as age, gender, and emotions
- Enhance or manipulate facial features for various applications, such as editing portraits or creating personalized avatars

### Demo Structure:

The demo application consists of two primary components:

1. **Console Python App**: A command-line application that retrieves an image from Azure Blob Storage, processes it using the Azure Face API to detect and measure the presence of a single face, and crops the image to a desired size.

2. **Web Page Example**: A sample webpage that showcases the results of the processing pipeline. The page displays:

    - Original and processed photos for comparison
    - Basic tests based on the output from the Azure Face API, including:
        - Blurriness detection: Is the picture blurry?
        - Occlusion detection: Are there any occlusions?
        - Glasses detection: Is the subject wearing glasses?
        - And more...

#### Console App (recommended):

The console application does not require user input; instead, it relies on environment variables to provide all necessary inputs.

This streamlined approach allows for easy deployment and testing of the app, as all required data is already configured and available through the [environment variables](#Environmental-Variables).

```
python3 ./app.py
```

## Setup

### Requirements

#### Python Packages

List of required Python packages. All are present in **requriements.txt** and can be installed from there.


```python
pip install -r ./requirements.txt
```


|package|description|
|---|---|
| [azure-cognitiveservices-vision-face](https://pypi.org/project/azure-cognitiveservices-vision-face/) | Microsoft Azure Cognitive Services Face Client Library |
| [azure-storage-blob](https://pypi.org/project/azure-storage-blob/) | Azure BLOB storage client library |
| [Pillow](https://pypi.org/project/pillow/) | Python image library |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Python-dotenv reads key-value pairs from a .env file and can set them as environment variables.|
| [Flask](https://pypi.org/project/Flask/) | _optional_ lightweight WSGI web application framework. _Only required for webapp_||



#### Environmental Variables

Using **example.env** as a template, create and populate **.env** to set required environmental variables. 

```
# Azure AI Face API 
VISION_ENDPOINT="https://<Azure Cognitive Services Vision API endpoint>.cognitiveservices.azure.com/"
VISION_KEY="<Azure Cognitive Services Vision API key>"

# SAS URL for the image (its going to expire)
PICTURE_URL="<URL with SAS token for source image>"

# Azure BLOB storage
AZURE_BLOB_ACCOUNT_NAME="<Azure Storage BLOB account name>"
AZURE_BLOB_CONTAINER_NAME="<Azure Storage BLOB container name>"
AZURE_BLOB_KEY="<Azure Storage BLOB key>"
AZURE_STORAGE_CONNECTION_STRING="<Azure Storage connection string>"

AZURE_BLOB_CONTAINER_PROCESSING_NAME="pass-images-processing"
AZURE_BLOB_ENDPOINT="<Azure Storage BLOB endpoint>"

```