import requests
import base64

url = "http://127.0.0.1:8000/api/predict/"

with open("test.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode('utf-8')

data = {
    "image": img_base64
}

response = requests.post(url, json=data)

print(response.json())