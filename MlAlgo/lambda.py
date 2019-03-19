import json
import boto3
import io
from PIL import Image
import queue
from ImageCropQueue import cropImage
from main import modelInfer

def handler(event, context): # Event comes in as a dict, with the users Bucket
                                    # and the users images name that was uploaded to the bucket
    
    # Create Queue
    q = queue.Queue(maxsize=1000)
    sentence = queue.Queue(maxsize=1000)
    sentenceString = " "

    # Crop image into words and add each word image to a queue
    q = cropImage(event.get('bucket'), event.get('image'))

    # Put image through CRNN
    for image in list(q.queue):
        sentence.put(modelInfer(image))
    
    # Get output as a string dict
    for word in list(sentence.queue):
        sentenceString += word + " "
    
    print(sentenceString)

    # Write string to file
    
    # Store file in s3 bucket
    
    # Transfer to json format
    
    # Send response

    return sentenceString
