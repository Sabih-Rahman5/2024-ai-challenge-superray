import cv2
# from basicsr.archs.rrdbnet_arch import RRDBNet
# from realesrgan import RealESRGANer
from ultralytics import YOLO
import requests
import base64

import numpy as np




def inference(image, classify_image):

    task = None
    # Get the dimensions (height, width, and number of channels)
    # height, width, channels = image.shape
    # height, width, channels = image.shape
    
    if (classify_image == 'chest'):
        task = 'xray'
        base_prompt = "Describe the xray image in detail. paying close attention to the lungs"
    if (classify_image == 'chest-ct'):       
        task = 'ct'
    if(classify_image == 'brain-mri'):
        task = 'mri'
    if(classify_image == 'limb-fracture'):
        task = 'fracture'


    # model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    # print("selected weights: ", weights)
    # upsampler = RealESRGANer(
    #     scale=4,
    #     model_path=('superrayapp/weights/' + str(weights)),
    #     dni_weight=None,
    #     model=model,
    #     tile=0,
    #     tile_pad=10,
    #     pre_pad=0,
    #     half=False,
    #     gpu_id=None
    # )
    
    

    # output, _ = upsampler.enhance(image, outscale=4)
    
    success, encoded_image = cv2.imencode('.png', image)

    base64_image = base64.b64encode(encoded_image).decode('utf-8')


    url = 'https://duly-resolved-stallion.ngrok-free.app/process_json'
    data = {
        "prompt": base_prompt,
        "image": base64_image,
        "task": task,
        "options": "ganllm",
    }
    print("requesting api...")
    response = requests.post(url, json=data)
    
    
    encoded_image = response.json()["upscaled_image"]
    print("image donloaded")
    
    
    image_bytes = base64.b64decode(encoded_image)
    nparr = np.frombuffer(image_bytes, np.uint8)
    print("runnin")
    upscaled_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # print(response.json()["response"])
    
    
    return upscaled_image, response.json()["response"]




def getImgClass(cv2_image):

    model = YOLO('superrayapp/weights/super_ray_general_classifier.pt')  
    
    results = model(cv2_image)  # predict on an image
    
    names_dict = results[0].names
    class_index = results[0].probs.top1
    prob = max(results[0].probs.data.tolist())
    print(prob)  
    
    prediction = (names_dict[class_index], prob)   
    
    return prediction[0]



def detect_fractures(image):
    
    print('reached till here')
    # print(image)
    model = YOLO("superrayapp/weights/super_ray_fracture_detect.pt")  
    
    
    cv2.imwrite("image.jpg", image)
    reloaded_image = cv2.imread("image.jpg")

    results = model.predict(reloaded_image, conf=0.3)  
    output_image = results[0].plot(labels=True, conf=False) 
    

    # cv2.imwrite('output.jpg', output_image)  
    
    print("detected fractures: ", len(results[0]))
    
    #return output_image, len(results[0])
    return output_image
    



# def chest_report(image, prompt):
#     url = 'https://duly-resolved-stallion.ngrok-free.app/process_json'
#     success, encoded_image = cv2.imencode('.png', image)

#     base64_image = base64.b64encode(encoded_image).decode('utf-8')
    
#     data = {
#     "prompt": prompt,
#     "image": base64_image
#     }
    
#     response = requests.post(url, json=data)
    
#     print(response)

#     print(response.json())