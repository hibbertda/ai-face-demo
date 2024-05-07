import os
import dotenv
import requests

# Load environment variables from .env file
dotenv.load_dotenv()

class AzureFaceAPI:
  def __init__(self):
    self.subscription_key = os.getenv('VISION_KEY')
    self.endpoint = os.getenv('VISION_ENDPOINT')
    self.face_api_url = f"{self.endpoint}/face/v1.0/detect"
    self.headers = {
      'Content-Type': 'application/json',
      'Ocp-Apim-Subscription-Key': self.subscription_key
    }
    self.params = {
      'returnFaceId': 'true',
      'returnFaceLandmarks': 'true',
      'returnFaceAttributes': 'noise,headPose,glasses,exposure,glasses,accessories,blur,occlusion',
      'detectionModel': 'detection_01',
      'recognitionModel': 'recognition_03'
    }

  def detect_faces(self, image_url):
    # REST API call to Azure Face API
    response = requests.post(
      self.face_api_url, 
      headers=self.headers, 
      params=self.params, 
      json={"url": image_url}
    )

    response.raise_for_status()
    return response.json()