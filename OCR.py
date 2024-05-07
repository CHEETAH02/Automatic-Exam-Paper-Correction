import json
import os
import requests
from autocorrect import Speller
from base64 import b64encode
from io import BytesIO
from PIL import Image

spell = Speller("en")

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


def requestOCR(image):
    image = Image.open(image)
    imgdata = make_image_data(image)
    ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
    api_key = os.environ.get('OCR_KEY')
    
    response = requests.post(ENDPOINT_URL, data=imgdata, params={'key': api_key}, headers={'Content-Type': 'application/json'})
    try:
        temp = response.json()['responses'][0]['textAnnotations'][0]['description']
        temp = temp.split("\n")
        response = ' '.join(temp)
        response = spell(response)
    except:
        response = ""
    return response
