import json
from base64 import b64encode
import requests
from PIL import Image
from io import BytesIO
from autocorrect import Speller

spell = Speller("en")

def bytes_to_image(data):
    img_byte_array = BytesIO(data)
    image = Image.open(img_byte_array)
    return image

def image_to_bytes(image):
    image = Image.open(image)
    img_byte_array = BytesIO()
    image.save(img_byte_array, format='PNG')
    img_bytes = img_byte_array.getvalue()
    return img_bytes

def make_image_data(pillow_image):
    img_req = None
    with BytesIO() as buffer:

        pillow_image.save(buffer, format="PNG")
        ctxt = b64encode(buffer.getvalue()).decode()
        img_req = {
            'image': {
                'content': ctxt
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": img_req}).encode()

def requestOCR(data):
    image = bytes_to_image(data)
    imgdata = make_image_data(image)
    ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
    api_key = "AIzaSyAl8wt0fVNGdi2tQ6qGCVLhvY9Fo_qxIgc"
    
    response = requests.post(ENDPOINT_URL, data = imgdata, params = {'key': api_key}, headers = {'Content-Type': 'application/json'})
    temp = []
    for index in range(1, len(response.json()['responses'][0]['textAnnotations'])):
        temp.append(response.json()['responses'][0]['textAnnotations'][index]['description'])
    response = ' '.join(temp)
    response = spell(response)
    # print(response)
    return response
