import cv2
from ultralytics import YOLO
import requests
import base64

import numpy as np




def inference(image, classify_image):


    """
    Perform inference on an image using a specified classification type.

    Args:
    - image: Image data to be processed.
    - classify_image: Type of image classification ('chest', 'chest-ct', 'brain-mri', 'limb-fracture').

    Returns:
    - upscaled_image: Processed image after inference.
    - response: Response from the API containing relevant information.
    """

    # Determine the task based on the classification type
    task = None
    if (classify_image == 'chest'):
        task = 'xray'
        base_prompt = "Describe the xray image in detail. paying close attention to the lungs"
    if (classify_image == 'chest-ct'):       
        task = 'ct'
    if(classify_image == 'brain-mri'):
        task = 'mri'
    if(classify_image == 'limb-fracture'):
        task = 'fracture'

    # Encode the image in PNG format
    success, encoded_image = cv2.imencode('.png', image)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')

    # Define API endpoint and prepare data for request
    url = 'https://duly-resolved-stallion.ngrok-free.app/process_json'
    data = {
        "prompt": base_prompt,
        "image": base64_image,
        "task": task,
        "options": "ganllm",
    }
    
    # Send a POST request to the API
    print("requesting api...")
    response = requests.post(url, json=data)
    
    # Decode the response and extract the upscaled image
    encoded_image = response.json()["upscaled_image"]
    print("image donloaded")
    
    # Decode the image bytes and process using OpenCV
    image_bytes = base64.b64decode(encoded_image)
    nparr = np.frombuffer(image_bytes, np.uint8)
    print("runnin")
    upscaled_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # print(response.json()["response"])
    
    # Return the processed image and response from the API
    return upscaled_image, response.json()["response"]




def getImgClass(cv2_image):
    
    """
    Get the class of an image using the YOLO object detection model.

    Args:
    - cv2_image: Image data in OpenCV format.

    Returns:
    - prediction: Class label predicted for the image.
    """

    # Load the YOLO model for image classification
    model = YOLO('superrayapp/weights/super_ray_general_classifier.pt')  
    # Predict using the loaded model
    results = model(cv2_image)  # predict on an image
    # Predict using the loaded model
    names_dict = results[0].names
    class_index = results[0].probs.top1
    prob = max(results[0].probs.data.tolist())
    print(prob)  
    
    # Get the predicted class and probability
    prediction = (names_dict[class_index], prob)   
    
    return prediction[0]



def detect_fractures(image):
    """
    Detect fractures in the given image using the YOLO object detection model.

    Args:
    - image: Image data to be analyzed.

    Returns:
    - output_image: Image with detected fractures highlighted.
    """

    print('Reached till here')
    
    # Load YOLO model for fracture detection
    model = YOLO("superrayapp/weights/super_ray_fracture_detect.pt")  
    
    # Save image temporarily and reload using OpenCV
    cv2.imwrite("image.jpg", image)
    reloaded_image = cv2.imread("image.jpg")

    # Perform prediction on the image
    results = model.predict(reloaded_image, conf=0.3)  

    # Plot the results on the image
    output_image = results[0].plot(labels=True, conf=False) 
    
    # Print the number of detected fractures
    print("Detected fractures: ", len(results[0]))
    
    return output_image
