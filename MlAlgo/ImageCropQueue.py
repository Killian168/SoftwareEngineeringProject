# @author: Killian O'Dálaigh
# @version: 31/01/2019
# Decription: Gets image and crops it into individual
# images of each word using AWS Rekognition to recognise each
# word

# Import Dependencies
import boto3
import json
import io
from PIL import Image
import queue

def cropImage(bucket, image):
     
        
    # Create Queue
    q = queue.Queue(maxsize=1000)
    
    # Connect to s3 and recieve picture
    bucket=bucket
    photo=image
    client=boto3.client('rekognition')

    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()

    # Change image to a bytes stream
    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)
    
    #Call DetectText
    response = json.dumps(client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}))

    # Get image size
    imgWidth, imgHeight = image.size

    # Read response into Json format
    a = json.loads(response)
    
    # Calculate the bounding box of each word      
    for entry in a['TextDetections']:
        
        # BoundingBox dimensions + padding variable
        box = entry['Geometry']['BoundingBox']
        left = imgWidth * box['Left'] +10
        top = imgHeight * box['Top']+10
        width = imgWidth* box['Width']+10
        height = imgHeight * box['Height']+10
        
        # Crop Bounding Box image and send onto queue
        
        # Points to crop on
        points = (
            left,
            top,
            (left + width),
            (top + height)
        )
        
        # Crop image and add it to the queue
        img1 = image.copy()
        img1 = img1.crop(points)
        img1.load()
        q.put(img1)

    return q