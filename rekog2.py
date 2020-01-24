import json
import boto3

def lambda_handler(event, context):
    # Change to your bucket Name!
    bucket= "ray1red-images"
    # If records are in it its an event from s3
    if "Records" in event:
        photo= event['Records'][0]['s3']['object']['key']
    else:
        # Add photo name from query parameter
        photo= event['queryStringParameters']['key']
    
    client=boto3.client('rekognition')

    # process using S3 object
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MinConfidence=85,
        MaxLabels=10)    


    #Get the labels
    labels=response['Labels']
    
    # return a browser freindly json object of the labels
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        }
        "body": labels
    }
    
    return response