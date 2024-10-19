# SageMaker endpoint for deeface

Straight forward implementation of SageMaker endpoint for hosting [deepface](https://github.com/serengil/deepface) api.

Based on: https://github.com/serengil/deepface/blob/master/deepface/api/src/modules/core/routes.py

# Local build and test

`docker build -t deepface-sm .`

`docker run -p 80:8080 deepface-sm /opt/program/serve`

`curl localhost/ping`

```
import base64
import cv2
import boto3
import json

# Load image in base64
def get_image_in_base64(image_file: str) -> str:
    img = cv2.imread(image_file)
    string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    img_base65 = f"data:image/jpg;base64,{string}"
    return img_base65

img1_base64: str = get_image_in_base64("steve-jobs.jpg")
img2_base64: str = get_image_in_base64("steve-2.jpg")

payload = {
    "service": "represent",
    "img_path": img_base64, 
}

x = requests.post("http://localhost/invocations", json = payload)

print(json.dumps(x.json(), indent=4))

```