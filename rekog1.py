import json
import boto3

def lambda_handler(event, context):
    # Change to your bucket Name!
    bucket= "ray1red-images"
    # Grap photo from s3 put event
    photo= event['Records'][0]['s3']['object']['key']
    
    client=boto3.client('rekognition')

    # process image using S3 object
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MinConfidence=85,
        MaxLabels=10)    

    #Get the labels
    labels=response
    # Log the labels
    print(labels)
    # return lables
    return {
        'statusCode': 200,
        'body': json.dumps(labels)
    }  
