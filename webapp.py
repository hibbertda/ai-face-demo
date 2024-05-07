import os
import uuid
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from werkzeug.utils import secure_filename
import requests

# Import local modules
from azfaceapi import AzureFaceAPI
from azstorage_operations import AzureBlobStorage, GenerateSASToken, GenerateContainerSASToken
from imageprocessor_operations import ImageProcessor

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/eval', methods=['GET'])
def eval():

    # open example json
    with open('./result.json') as f:
        data = json.load(f)

    return render_template('eval.html', data=data)

# Upload image
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')


@app.route('/api/getcontainersas', methods=['POST'])
def generate_sas():
    # Parameters
    container_name = os.getenv('AZURE_BLOB_CONTAINER_PROCESSING_NAME')
    blob_name = 'unique_blob_name'  # This could be dynamic based on the filename
    blob_endpoint = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net"
    
    # Generate SAS token
    sas_token = GenerateContainerSASToken.generate_sas_token(
        os.getenv('AZURE_STORAGE_ACCOUNT_NAME'),
        container_name
    )

    # JSON response
    return jsonify({
        "sas_token": sas_token,
        "container_name": container_name,
        "blob_endpoint": blob_endpoint,
        #"blob_name": blob_name,
        "expiry": datetime.utcnow() + timedelta(hours=1),  # Include expiry time
        "content_type": "image/jpeg",  # Specify expected content type
    }), 200

if __name__ == '__main__':
    app.run(
       debug=True,
       port=5055
       )
