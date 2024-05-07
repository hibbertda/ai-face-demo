from PIL import Image, ImageDraw

class ImageProcessor:
  def __init__(self):
    pass

  def resize_image(self, image, faces):
    # Find the coordinates of the tip of the nose
    nose_tip = None
    for face in faces:
      landmarks = face['faceLandmarks']
      nose_tip = (landmarks['noseTip']['x'], landmarks['noseTip']['y'])
      break
    
    # Calculate the crop dimensions
    crop_width = crop_height = 2 * image.info['dpi'][0]  # Assuming dpi is in pixels per inch
    crop_left = int(nose_tip[0] - crop_width / 2)
    crop_top = int(nose_tip[1] - crop_height / 2)
    crop_right = crop_left + crop_width
    crop_bottom = crop_top + crop_height
    
    # Crop the image
    cropped_image = image.crop((crop_left, crop_top, crop_right, crop_bottom))
    
    # Resize the cropped image to 2in by 2in
    resized_image = cropped_image.resize((2 * image.info['dpi'][0], 2 * image.info['dpi'][0]))
    
    return resized_image

  def draw_faces(self, image, faces):
    draw = ImageDraw.Draw(image)
    for face in faces:
      rect = face['faceRectangle']
      left, top, width, height = rect['left'], rect['top'], rect['width'], rect['height']
      right, bottom = left + width, top + height
      draw.rectangle([left, top, right, bottom], outline='red', width=3)
    return image