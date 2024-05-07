import os
import dotenv
import requests
from PIL import Image, ImageDraw
import json

from azfaceapi import AzureFaceAPI
from azstorage_operations import AzureBlobStorage, GenerateSASToken
from imageprocessor_operations import ImageProcessor

# Load environment variables from .env file
dotenv.load_dotenv()
  

if __name__ == "__main__":
  # Initialize API client
  api_client = AzureFaceAPI()
  original_image_url = ""
  image_url = os.getenv('PICTURE_URL')

  try:
    # Fetch face details from the image
    faces = api_client.detect_faces(image_url)

    # If more than one face is detected, return a message to the user
    if len(faces) > 1:
      print("More than one face detected. Please upload an image with only one face.")
      exit()

    #print(json.dumps(faces, indent=2))
  except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")

  # Print image image dimensions 
  image = Image.open(requests.get(image_url, stream=True).raw)
  print(f"Image dimensions: {image.size}")

  # If image is larger that 300x300 resize based on the face detected in the image
  if image.size[0] > 300 and image.size[1] > 300:
    original_image_url = image_url
    cropped_image = ImageProcessor().resize_image(image, faces)
    cropped_image.save("resized_image.jpg")

    # Upload cropped image to Azure Blob Storage and get SAS Token
    upload =  AzureBlobStorage().upload_image(cropped_image, faces[0]['faceId'])
    image_url = upload['image_url']

    # Re-detect faces in the cropped image
    faces = api_client.detect_faces(image_url)
    #image = Image.open(requests.get(image_url, stream=True).raw)
    #print(f"Image dimensions: {image.size}")
  
  # Else proceed with the face detection

  # If no face is detected, return a message to the user

  # Else proceed with the face detection    

  sas_token = GenerateSASToken().generate_sas_token(upload['image_url'])
  image_url_sas = {image_url} + "?" + sas_token
  image = Image.open(requests.get(image_url_sas, stream=True).raw)

  # Process image
  img = ImageProcessor().draw_faces(image, faces)
  img.save("detected_faces.jpg")


# Create JSON document with the original image URL and the processed image URL
  result = {
    "original_image_url": original_image_url,
    "processed_image_url": upload['image_url'],
    "id": faces[0]['faceId'],
    "faceRectangle": faces[0]['faceRectangle'],
    "faceLandmarks": faces[0]['faceLandmarks'],
    "faceAttributes": faces[0]['faceAttributes']
  }

  with open('result.json', 'w') as f:
    json.dump(result, f, indent=2)

  print("Faces have been marked and the image has been saved.")
  print("Results have been saved to result.json")