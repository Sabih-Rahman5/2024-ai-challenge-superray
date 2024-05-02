# SuperRay: Web App for X-ray image Up-Scaling and Diagnostics

SuperRay is a web application designed for up-scaling and diagnostics. The application is divided into two main components: the backend built with Django (Python) and the front-end built with Next.js and Tailwind CSS (JavaScript).
## Installation


### Requirements
python 3.10

node v21.6.1

Clone of the repository:


```bash
git clone https://github.com/Sabih-Rahman5/2024-ai-challenge-superray.git
```
### Backend (Django)




1. navigate to the SuperRay-Backend folder
```
cd SuperRay-Backend
```



2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
```

3. Activate Environment:

```bash
.venv/Scripts/Activate
```
4. Install the required packages by running pip install -r requirements.txt:
```bash
pip install -r requirements.txt
```

5. Run Server:

```bash
python manage.py runserver
```

The backend development server should now be running at http://localhost:8000 with the following routes:

•	/admin

•	/api for super resolution

•	/api for login

•	/api for token refresh

•	/api for register

•	/api for logout

•	/api for to view profile

•	/api for update profile



### Front-end(Next-js)

1. Navigate to the SuperRay-NextJs-Tailwind directory:


```bash
cd SuperRay-NextJs-Tailwind
```



2. Install dependencies:


```bash
npm install
```
3. Start the development server:
```
npm run dev
```


The frontend development server should now be running at http://localhost:3000.


P.S. refer views.py and functions.py for functionality implementations

following is the code for remote server:

```
from flask import Flask, request, jsonify
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
import time
import cv2
import torch


app = Flask(__name__)

@app.route('/process_json', methods=['POST'])
def process_json():
    # Get the JSON data from the request
    json_data = request.get_json()

    # Check if JSON data is present
    if not json_data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    encoded_image = str(json_data["image"])
    
    image_bytes = base64.b64decode(encoded_image)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    
    response_data = {
        "response": "response"
    }
    
    
    if json_data["options"] == "gan" or json_data["prompt"] == None:
        upscaled_image = upscale(image, json_data["task"])
        success, encoded_image = cv2.imencode('.png', upscaled_image)
        base64_image = base64.b64encode(encoded_image).decode('utf-8')
        response_data = {
            "response": "None",
            "upscaled_image": base64_image,
        }
        
        
    elif json_data["options"] == "llm":
        prompty = json_data["prompt"]
        response = chest(image, prompty)
        
        
        
        response_data = {
            "response": response
        }
            
    elif json_data["options"] == "ganllm":
        upscaled_image = upscale(image, json_data["task"])
        success, encoded_image = cv2.imencode('.png', upscaled_image)
        base64_image = base64.b64encode(encoded_image).decode('utf-8')
        prompty = json_data["prompt"]
        response = chest(image, prompty)
        print(response)
        response_data = {
            "response": response,
            "upscaled_image": base64_image,
        }
    
    
    else:
        response_data = {
            "response": "Error incorrect task",
        }
    
    
    inputs = None
    torch.cuda.empty_cache()
    

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

















