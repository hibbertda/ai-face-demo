
import os
import dotenv
from datetime import timedelta, datetime
from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions, ContentSettings, generate_blob_sas
from io import BytesIO
from urllib.parse import urlparse

# Load environment variables from .env file
dotenv.load_dotenv()

class AzureBlobStorage:
  def __init__(self):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

  def upload_image(self, image, file_name):

    container_name = os.getenv('AZURE_BLOB_CONTAINER_PROCESSING_NAME')
    blob_name = f'{file_name}.jpeg'
    blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    

    byte_stream = BytesIO()
    image.save(byte_stream, format='JPEG')
    byte_stream.seek(0)

    blob_client.upload_blob(
      byte_stream, 
      content_settings=ContentSettings(content_type='image/jpeg'))

    # Get uploaded file url
    image_url = f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"

    # Generate a SAS token for the uploaded image
    sas_token = generate_blob_sas(
      self.blob_service_client.account_name,
      container_name,
      blob_name,
      account_key=self.blob_service_client.credential.account_key,
      permission=ContainerSasPermissions(read=True),
      expiry=datetime.utcnow() + timedelta(hours=1)
    )
    
    # Return the image URL and SAS token as dict
    return {
      "image_url": image_url,
      "sas_token": sas_token
    }

class GenerateSASToken:
  def __init__(self):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

  def generate_sas_token(self, image_url):
    parsed_url = urlparse(image_url)
    container_name = parsed_url.path.split('/')[1]
    blob_name = parsed_url.path.split('/')[2]

    sas_token = generate_blob_sas(
      self.blob_service_client.account_name,
      container_name,
      blob_name,
      account_key=self.blob_service_client.credential.account_key,
      permission=ContainerSasPermissions(read=True),
      expiry=datetime.utcnow() + timedelta(hours=1)
    )
    return sas_token

class GenerateContainerSASToken:
  def __init__(self):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
  
  def generate_sas_token(self, container_name):
    sas_token = generate_container_sas(
      self.blob_service_client.account_name,
      container_name,
      account_key=self.blob_service_client.credential.account_key,
      permission=ContainerSasPermissions(read=True, write=True),
      expiry=datetime.utcnow() + timedelta(hours=1)
    )
    return sas_token
